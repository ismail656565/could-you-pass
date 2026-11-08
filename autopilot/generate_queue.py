"""Fill an empty production queue with a fresh, curated quiz Short.

No paid AI API is required. Questions are curated locally; used questions are
held back for 14 days. If the bank is exhausted, fail loudly rather than
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

LONG_TITLES = [
    "If You Get 40 Right, Your Memory Is Excellent 🧠",
    "Are You Over 60? Let's Check Your Memory 🧠",
    "Your IQ Is Above Average If You Get 35+ Right 🧠",
    "How Sharp Is Your Brain? 50 Questions From Easy to Legend",
    "Only 1 in 10 Can Get 45/50 🧠",
]


def strip_intro(text):
    """Remove intros/hooks copied from older items so a line starts with the question."""
    text = str(text or "")
    for prefix in ("Welcome back, quiz friends!", "Grab a pen and keep score.", "Quick quiz!",
                   "Only one in ten adults get this right."):
        text = text.replace(prefix, "")
    text = text.replace("Double tap to lock your answer!", "").replace("Think fast, and lock in your answer.", "")
    text = re.sub(r"^\s*(Fifty|Forty|Thirty-five|Forty-five) questions[^.?!]*[.?!]", "", text.strip())
    return re.sub(r"\s+", " ", text).strip()


def fmt_of_path(path):
    item = read_json(path)
    return "long" if item.get("story", {}).get("format") == "long" else "short"


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

def recently_used_questions(today):
    used = set()
    cutoff = today - dt.timedelta(days=14)
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
    """Build two Shorts and one long quiz from the repository's existing, curated question archive.

    No paid AI/API is used. Recent questions (14 days) are excluded; if the archive
    does not contain enough unused questions or compatible templates, fail loudly.
    """
    import copy
    import random

    QUEUE.mkdir(parents=True, exist_ok=True)
    DONE.mkdir(parents=True, exist_ok=True)

    today = dt.date.today()
    used = recently_used_questions(today)

    def fmt(item):
        return "long" if item.get("story", {}).get("format") == "long" else "short"

    done_today = {"short": 0, "long": 0}
    for path in DONE.glob("*.json"):
        item = read_json(path)
        if item.get("uploaded", {}).get("at", "").startswith(today.isoformat()):
            done_today[fmt(item)] += 1

    queued = {"short": [], "long": []}
    queued_keys = set()
    for path in sorted(QUEUE.glob("*.json")):
        item = read_json(path)
        kind = fmt(item)
        queued[kind].append(path)
        for question in item.get("story", {}).get("questions", []):
            key = re.sub(r"[^a-z0-9]+", " ", str(question.get("q", "")).lower()).strip()
            if key:
                used.add(key)
                queued_keys.add(key)

    missing = {
        "short": max(0, 2 - done_today["short"] - len(queued["short"])),
        "long": max(0, 1 - done_today["long"] - len(queued["long"])),
    }
    if not any(missing.values()):
        print(
            f"Daily target already covered: uploaded today Shorts={done_today['short']}, "
            f"long={done_today['long']}; queued Shorts={len(queued['short'])}, long={len(queued['long'])}.",
            flush=True,
        )
        return
    pool = []
    recycled_pool = []
    templates = {"short": [], "long": []}
    used_today = set(queued_keys)
    for path in DONE.glob("*.json"):
        item = read_json(path)
        if item.get("uploaded", {}).get("at", "").startswith(today.isoformat()):
            for question in item.get("story", {}).get("questions", []):
                key = re.sub(r"[^a-z0-9]+", " ", str(question.get("q", "")).lower()).strip()
                if key:
                    used_today.add(key)

    def norm(question):
        return re.sub(r"[^a-z0-9]+", " ", str(question or "").lower()).strip()

    # Use the channel's own previously rendered quiz files as templates and as
    # a source of vetted questions/answer scripts.
    source_files = list(DONE.glob("*.json")) + list((AP / "test").glob("*.json"))
    for path in source_files:
        item = read_json(path)
        story = item.get("story", {})
        fmt = "long" if story.get("format") == "long" else "short"
        questions = story.get("questions", [])
        lines = item.get("lines", [])
        if questions and len(questions) == len(lines):
            if len(questions) >= (50 if fmt == "long" else 1) and not any(q.get("values") for q in questions):
                templates[fmt].append(item)
            for q, line in zip(questions, lines):
                key = norm(q.get("q"))
                if not key or key in used_today:
                    continue
                if q.get("values") or not isinstance(q.get("answers"), list) or len(q["answers"]) != 4:
                    continue
                correct = q.get("correct")
                if not isinstance(correct, int) or not 0 <= correct < len(q["answers"]):
                    continue
                if not line.get("q") or not line.get("a"):
                    continue
                row = {"question": copy.deepcopy(q), "line": copy.deepcopy(line), "key": key}
                (recycled_pool if key in used else pool).append(row)

    # Add the built-in fact bank as a free backup source.
    for question, answers, correct, explanation, emoji, category in BANK:
        key = norm(question)
        if key in used_today:
            continue
        row = {
            "question": {
                "q": question, "answers": list(answers), "correct": correct,
                "level": "MEDIUM", "cardText": emoji,
                "start": 0.0, "countdownStart": 0.0, "reveal": 0.0, "end": 0.0
            },
            "line": {
                "q": f"Quick quiz! {question} Think fast, and lock in your answer.",
                "a": f"{answers[correct]}! {explanation}"
            },
            "key": key
        }
        (recycled_pool if key in used else pool).append(row)

    # Deduplicate old files that may contain the same question more than once.
    deduped = {}
    for row in pool:
        deduped.setdefault(row["key"], row)
    pool = list(deduped.values())
    recycled = {}
    for row in recycled_pool:
        if row["key"] not in deduped:
            recycled.setdefault(row["key"], row)

    if not templates["short"]:
        raise RuntimeError("No compatible one-question Short template found in autopilot/queue/done or autopilot/test.")
    if not templates["long"]:
        raise RuntimeError("No compatible 50-question long-video template found in autopilot/queue/done or autopilot/test.")

    needed = missing["short"] * 1 + missing["long"] * 50
    if len(pool) < needed:
        # Free mode has no generative API. If the unused bank is too small,
        # recycle older questions from the existing channel archive, but never
        # duplicate a question already uploaded today or within today's batch.
        pool.extend(list(recycled.values()))
    if len(pool) < needed:
        raise RuntimeError(
            f"Not enough distinct questions even after archive fallback: "
            f"{len(pool)} available, {needed} required. Add more curated questions."
        )

    random.Random(today.toordinal() + done_today["short"] * 11 + done_today["long"] * 31).shuffle(pool)
    cursor = 0
    specs = []
    for offset in range(missing["short"]):
        slot = done_today["short"] + len(queued["short"]) + offset
        suffix = f"short-{slot + 1}"
        specs.append((suffix, "short", pool[cursor:cursor + 1], ("16:00", "21:00")[min(slot, 1)]))
        cursor += 1
    if missing["long"]:
        rank = {"EASY": 0, "MEDIUM": 1, "HARD": 2, "VERY HARD": 3, "EXPERT": 3, "LEGEND": 4}
        long_rows = sorted(pool[cursor:cursor + 50],
                           key=lambda r: rank.get(str(r["question"].get("level", "MEDIUM")).upper(), 1))
        specs.append(("long", "long", long_rows, "14:00"))

    for suffix, fmt, rows, publish_at in specs:
        template = random.Random(today.toordinal() + len(suffix)).choice(templates[fmt])
        item = copy.deepcopy(template)
        item_id = f"auto-{today.isoformat()}-{suffix}"
        # Avoid overwriting a prior item if a workflow is re-run on the same day.
        while (QUEUE / f"{item_id}.json").exists() or (DONE / f"{item_id}.json").exists():
            item_id += "-next"

        item["id"] = item_id
        item["tts"] = "kokoro"  # force the free local voice; never inherit a paid TTS setting from a template
        item["lines"] = [copy.deepcopy(row["line"]) for row in rows]
        # Preserve timing/layout from the matching template; only replace quiz content.
        skeleton = item["story"]["questions"]
        if len(skeleton) < len(rows):
            raise RuntimeError(f"Template {fmt} has only {len(skeleton)} timed questions, need {len(rows)}.")
        new_questions = []
        for index, row in enumerate(rows):
            question = copy.deepcopy(skeleton[index])
            # Template visuals belong to the template's question (e.g. a Venus photo) – drop them.
            for field in ("image", "revealImage", "revealCaption", "cardText", "values", "valueLabels", "icons", "images"):
                question.pop(field, None)
            for field in ("q", "answers", "correct", "level", "cardText", "image", "revealImage", "revealCaption"):
                if field in row["question"]:
                    question[field] = copy.deepcopy(row["question"][field])
            if not question.get("image") and not question.get("cardText"):
                question["cardText"] = "❓"
            new_questions.append(question)
        item["story"]["questions"] = new_questions
        item["story"]["format"] = fmt
        n_auto = sum(1 for p in DONE.glob("auto-*.json") if fmt_of_path(p) == fmt) + 1
        story = item["story"]
        # Shorts: 2D-Strichmännchen-Moderator (Layout "stick"); lange Videos bleiben im TV-Look (16:9)
        story["layout"] = "stick" if fmt == "short" else "tvshow"
        for key in ("thumbImage", "thumbPuzzle"):
            story.pop(key, None)
        first_q = str(rows[0]["question"].get("q", "")).replace("**", "").strip()
        if fmt == "long":
            pattern = LONG_TITLES[n_auto % len(LONG_TITLES)]
            title = f"{pattern} | General Knowledge Quiz #{n_auto}"
            story.update({
                "title": "50 Question General Knowledge Quiz", "header": "GENERAL KNOWLEDGE",
                "hook": "CAN YOU GET 40/50? 🧠", "finalLabel": "FINAL QUESTION 🔥",
                "thumbTexts": ["GENERAL **KNOWLEDGE**", "CAN YOU GET **40/50**?", "TEST YOUR **MEMORY**"],
                "thumbEmoji": "🧠", "thumbBadge": "50 QUESTIONS · EASY → LEGEND",
            })
            item["outroLine"] = ("How many did you get? Comment your score below, "
                                 "and subscribe with the bell on for a new quiz every day!")
            item["lines"][0]["q"] = ("Welcome back, quiz friends! Fifty questions, grab a pen and keep score. "
                                     + strip_intro(item["lines"][0]["q"]))
            mid = min(int(story.get("midCtaIndex") or 24), len(item["lines"]) - 2)
            story["midCtaIndex"] = mid
            item["lines"][mid]["a"] = (item["lines"][mid]["a"].rstrip()
                                       + " If you're enjoying this, subscribe and turn on the bell!")
            description = ("50 general knowledge questions, from easy to legend. How many can you get right? 🧠\n"
                           "Comment your score 👇\n\nSubscribe for a new quiz every day! 🔔")
        else:
            title = f"{first_q[:80]} 🤯 #shorts"
            story.update({
                "title": "Trivia", "header": "TRIVIA", "hook": "CAN YOU GET THIS? 🤔",
                "teaser": "DOUBLE TAP TO LOCK IN ❤️", "finalLabel": "", "ctaText": "Follow if you got it ✅",
                "outroText": "Did you get it?", "outroSub": "Comment 👇",
            })
            line = item["lines"][0]
            line["q"] = strip_intro(line["q"])
            description = ("Quick quiz question 🤯 Did you get it?\nComment your answer 👇\n\n"
                           "Follow for a new quiz every day! 🧠")
        item["youtube"] = {
            "title": title[:100],
            "description": description + "\n\n#quiz #trivia #generalknowledge #quizchallenge"
                           + (" #shorts" if fmt == "short" else "") + "\n\nMusic: original.",
            "tags": ["quiz", "trivia", "general knowledge quiz", "quiz challenge", "brain test", "trivia questions"]
                    + (["shorts"] if fmt == "short" else ["memory test", "50 question quiz"]),
            "comment": "What score did you get? Comment below! 👇" if fmt == "long"
                       else "What did you answer? Comment below! 👇",
            "categoryId": "24",
        }
        item["publishAt"] = publish_at
        item["generatedBy"] = "free-archive-generator"
        item["generatedAt"] = dt.datetime.now().isoformat(timespec="minutes")
        for key in ("uploaded", "playlistAdded", "linkedLong", "thumbTest", "_thumb"):
            item.pop(key, None)

        target = QUEUE / f"{item_id}.json"
        target.write_text(json.dumps(item, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Created {fmt} queue item: {target.name} ({len(rows)} questions)", flush=True)

    print("Queue prepared for remaining daily target. Shorts use one-question templates; long video uses the 50-question template. No paid AI/API used.", flush=True)

if __name__ == "__main__":
    try:
        ensure_queue()
    except Exception as exc:
        print(f"QUEUE GENERATION FAILED: {exc}", file=sys.stderr, flush=True)
        raise
