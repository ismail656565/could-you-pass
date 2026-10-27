"""Fill an empty production queue with a fresh, curated quiz Short.

No paid AI API is required. Questions are curated locally; used questions are
held back for 30 days. If the bank is exhausted, fail loudly rather than
silently reporting a successful run with no video.
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AP = ROOT / "autopilot"
QUEUE = AP / "queue"
DONE = QUEUE / "done"
FAILED = QUEUE / "failed"

# One-question quizzes are intentionally short and self-contained. Keep facts
# stable and avoid time-sensitive/current-affairs questions.
BANK = [
    ("How many hearts does an octopus have?", ["One", "Two", "Three", "Four"], 2, "Three! Two pump blood to the gills, and one pumps it to the body.", "🐙", "NATURE"),
    ("Which planet has the most moons confirmed so far?", ["Earth", "Mars", "Saturn", "Mercury"], 2, "Saturn! The confirmed count changes as astronomers discover more, so this fact can change.", "🪐", "SPACE"),
    ("What is the largest mammal on Earth?", ["African elephant", "Blue whale", "Giraffe", "Orca"], 1, "The blue whale! It is the largest animal known to have lived on Earth.", "🐋", "NATURE"),
    ("Which gas do plants absorb from the air?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Helium"], 2, "Carbon dioxide! Plants use it, water and light during photosynthesis.", "🌿", "SCIENCE"),
    ("How many sides does a hexagon have?", ["Five", "Six", "Seven", "Eight"], 1, "Six! The prefix hexa means six.", "🔷", "BRAIN"),
    ("Which ocean is the largest?", ["Atlantic", "Indian", "Arctic", "Pacific"], 3, "The Pacific Ocean! It is larger than all of Earth's land area combined.", "🌊", "GEOGRAPHY"),
    ("What is the chemical symbol for gold?", ["Go", "Gd", "Au", "Ag"], 2, "Au! It comes from the Latin word aurum.", "🥇", "SCIENCE"),
    ("Which bird is famous for being able to fly backwards?", ["Eagle", "Hummingbird", "Penguin", "Ostrich"], 1, "The hummingbird! It can hover and fly backwards.", "🐦", "NATURE"),
    ("What is the hardest natural substance?", ["Quartz", "Iron", "Diamond", "Granite"], 2, "Diamond! It ranks highest on the traditional Mohs hardness scale.", "💎", "SCIENCE"),
    ("How many minutes are in a full day?", ["1,240", "1,340", "1,440", "1,540"], 2, "One thousand four hundred and forty minutes: 24 hours times 60.", "⏰", "BRAIN"),
    ("Which country is shaped like a boot?", ["Greece", "Italy", "Portugal", "Croatia"], 1, "Italy! Its peninsula is famously described as a boot.", "🇮🇹", "GEOGRAPHY"),
    ("What is the smallest prime number?", ["0", "1", "2", "3"], 2, "Two! It is the only even prime number.", "🔢", "BRAIN"),
    ("Which metal is liquid at ordinary room temperature?", ["Copper", "Mercury", "Aluminium", "Silver"], 1, "Mercury! It is a metal that remains liquid at typical room temperatures.", "🌡️", "SCIENCE"),
    ("What is the capital of Australia?", ["Sydney", "Melbourne", "Canberra", "Perth"], 2, "Canberra! Sydney and Melbourne are larger, but neither is the capital.", "🇦🇺", "GEOGRAPHY"),
    ("Which organ pumps blood around your body?", ["Liver", "Lungs", "Heart", "Kidneys"], 2, "Your heart! It circulates blood through the body's blood vessels.", "❤️", "BODY"),
    ("What do bees collect from flowers to make honey?", ["Pollen only", "Nectar", "Sap", "Dew"], 1, "Nectar! Bees process nectar into honey; pollen is mainly a protein source.", "🐝", "NATURE"),
    ("Which is the closest star to Earth?", ["Sirius", "The Sun", "Proxima Centauri", "Polaris"], 1, "The Sun! Proxima Centauri is the closest star beyond our solar system.", "☀️", "SPACE"),
    ("How many bones are typically in an adult human body?", ["106", "206", "306", "406"], 1, "About 206! Babies have more bones, many of which fuse as they grow.", "🦴", "BODY"),
    ("Which language has the most native speakers worldwide?", ["English", "Spanish", "Mandarin Chinese", "Hindi"], 2, "Mandarin Chinese has the most native speakers; rankings differ if second-language speakers are included.", "🗣️", "LANGUAGE"),
    ("What is the freezing point of pure water at standard pressure?", ["0°C", "10°C", "32°C", "100°C"], 0, "Zero degrees Celsius, which is 32 degrees Fahrenheit.", "🧊", "SCIENCE"),
    ("Which animal is the tallest living land animal?", ["Camel", "Ostrich", "Giraffe", "Elephant"], 2, "The giraffe! Its long neck helps it reach leaves high in trees.", "🦒", "NATURE"),
    ("What is the main gas in Earth's atmosphere?", ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], 2, "Nitrogen, making up about 78 percent of dry air.", "🌍", "SCIENCE"),
    ("Which continent has the most countries?", ["Asia", "Europe", "Africa", "South America"], 2, "Africa! It has 54 widely recognized sovereign states.", "🌍", "GEOGRAPHY"),
    ("What is the square root of 144?", ["10", "11", "12", "14"], 2, "Twelve! Twelve times twelve equals 144.", "➗", "BRAIN"),
    ("Which planet is known as the Red Planet?", ["Venus", "Mars", "Jupiter", "Mercury"], 1, "Mars! Iron-rich dust gives its surface a reddish appearance.", "🔴", "SPACE"),
    ("Which vitamin can the body produce after sunlight exposure?", ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D"], 3, "Vitamin D! UVB exposure helps the skin produce it.", "🌞", "BODY"),
    ("What is the largest hot desert in the world?", ["Gobi", "Sahara", "Arabian", "Kalahari"], 1, "The Sahara! Antarctica is the world's largest desert overall, but it is a polar desert.", "🏜️", "GEOGRAPHY"),
    ("Which instrument measures air pressure?", ["Thermometer", "Barometer", "Anemometer", "Hygrometer"], 1, "A barometer! Meteorologists use air pressure to help track weather.", "🌦️", "SCIENCE"),
    ("How many players from one team are on a football pitch at kickoff?", ["9", "10", "11", "12"], 2, "Eleven per team, including the goalkeeper.", "⚽", "SPORT"),
    ("Which is the largest internal organ in the human body?", ["Brain", "Liver", "Lung", "Stomach"], 1, "The liver! The skin is the largest organ overall.", "🫀", "BODY"),
    ("What is the currency of Japan?", ["Won", "Yuan", "Yen", "Baht"], 2, "The yen! Its symbol is ¥.", "💴", "GEOGRAPHY"),
    ("Which planet is famous for its prominent rings?", ["Earth", "Mars", "Saturn", "Venus"], 2, "Saturn! Other giant planets also have rings, but Saturn's are especially prominent.", "🪐", "SPACE"),
    ("What is the process called when liquid water becomes vapour?", ["Condensation", "Freezing", "Evaporation", "Melting"], 2, "Evaporation! It changes liquid water into water vapour.", "💧", "SCIENCE"),
    ("Which mammal lays eggs?", ["Koala", "Platypus", "Dolphin", "Bat"], 1, "The platypus! Echidnas are another egg-laying mammal group.", "🥚", "NATURE"),
    ("How many degrees are in a right angle?", ["45", "90", "180", "360"], 1, "Ninety degrees! A straight angle is 180 degrees.", "📐", "BRAIN"),
    ("Which country gifted the Statue of Liberty to the United States?", ["France", "Italy", "Canada", "Spain"], 0, "France! The statue was dedicated in New York in 1886.", "🗽", "HISTORY"),
    ("What is the largest species of big cat?", ["Lion", "Leopard", "Tiger", "Cheetah"], 2, "The tiger! Adult males of some tiger populations are the largest big cats.", "🐅", "NATURE"),
    ("Which blood cells help fight infection?", ["Red blood cells", "White blood cells", "Platelets", "Plasma cells only"], 1, "White blood cells! Different types help the immune system fight infection.", "🩸", "BODY"),
    ("What is the capital of Canada?", ["Toronto", "Vancouver", "Ottawa", "Montreal"], 2, "Ottawa! Toronto is Canada's largest city, but not its capital.", "🇨🇦", "GEOGRAPHY"),
    ("Which force keeps planets in orbit around the Sun?", ["Magnetism", "Friction", "Gravity", "Electricity"], 2, "Gravity! It keeps planets bound to the Sun while they move through space.", "🌌", "SPACE"),
]

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

def recently_used_questions(today):
    used = set()
    cutoff = today - dt.timedelta(days=30)
    for path in DONE.glob("*.json"):
        item = read_json(path)
        uploaded = item.get("uploaded", {}).get("at", "")
        try:
            when = dt.date.fromisoformat(uploaded[:10])
        except ValueError:
            continue
        if when < cutoff:
            continue
        for q in item.get("story", {}).get("questions", []):
            used.add(re.sub(r"[^a-z0-9]+", " ", q.get("q", "").lower()).strip())
    return used

def ensure_queue():
    QUEUE.mkdir(parents=True, exist_ok=True)
    DONE.mkdir(parents=True, exist_ok=True)
    if any(QUEUE.glob("*.json")):
        print("Queue already contains work; no fallback quiz needed.", flush=True)
        return
    today = dt.date.today()
    used = recently_used_questions(today)
    available = [row for row in BANK if re.sub(r"[^a-z0-9]+", " ", row[0].lower()).strip() not in used]
    if not available:
        raise RuntimeError("Quiz question bank exhausted: no unused question in the last 30 days. Add new verified questions; refusing to upload a repeat.")
    # Rotate deterministically by date, but skip recently-used questions.
    index = (today.toordinal() * 7) % len(available)
    question, answers, correct, explanation, emoji, category = available[index]
    slug = re.sub(r"[^a-z0-9]+", "-", question.lower()).strip("-")[:42]
    item_id = f"auto-{today.isoformat()}-{slug}"
    while (QUEUE / f"{item_id}.json").exists() or (DONE / f"{item_id}.json").exists():
        item_id += "-next"
    correct_answer = answers[correct]
    item = {
        "id": item_id,
        "timing": {"count": 3.0, "tail": 0.5, "tempo": 1.0},
        "lines": [{
            "q": f"Quick quiz! {question} Think fast, and lock in your answer.",
            "a": f"{correct_answer}! {explanation} Follow for another quick quiz."
        }],
        "youtube": {
            "title": f"Can You Get This {category.title()} Question Right? 🤯 #shorts",
            "description": f"One quick question. Did you know the answer?\nComment your guess below.\n\nFollow for a new quiz every day! 🧠\n\n#quiz #trivia #generalknowledge #funfacts #shorts",
            "tags": ["quiz", "trivia", "general knowledge quiz", category.lower() + " quiz", "fun facts", "shorts"],
            "comment": f"Did you get it right? The answer was {correct_answer}. 👇"
        },
        "story": {
            "type": "quiz", "format": "short", "layout": "tvshow",
            "title": "Quick Quiz", "header": f"{category} QUIZ",
            "hook": "CAN YOU GET THIS RIGHT? 🤯",
            "teaser": "LOCK IN YOUR ANSWER 👇",
            "finalLabel": "", "ctaText": "Follow for another quiz ✅",
            "correctLabel": "CORRECT!", "revealIcon": emoji,
            "music": "sfx/game-show.wav", "musicVolume": 0.1,
            "outroText": "Did you get it?", "outroSub": "Comment below 👇",
            "questions": [{
                "q": question, "answers": answers, "correct": correct,
                "level": "MEDIUM", "cardText": emoji,
                "start": 0.0, "countdownStart": 0.0, "reveal": 0.0, "end": 0.0
            }]
        },
        "publishAt": "16:00",
        "generatedBy": "curated-fallback",
        "generatedAt": dt.datetime.now().isoformat(timespec="minutes")
    }
    target = QUEUE / f"{item_id}.json"
    target.write_text(json.dumps(item, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Created fallback quiz: {target.name}", flush=True)

if __name__ == "__main__":
    try:
        ensure_queue()
    except Exception as exc:
        print(f"QUEUE GENERATION FAILED: {exc}", file=sys.stderr, flush=True)
        raise
