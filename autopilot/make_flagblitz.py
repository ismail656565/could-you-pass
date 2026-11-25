"""Baut ein Flaggen-Long „Guess the Flag in 3 Seconds – Easy to Impossible“ (story.type "flagblitz").
Aufruf:  python autopilot/make_flagblitz.py <id> <datum YYYY-MM-DD> [anzahl pro Level, Standard 25] [--demo]
Schreibt autopilot/queue/<datum>-<id>.json (14:00, Long). Mit --demo nur stories/<id>.json (Vorschau).
Flaggen, die in früheren flagblitz-Folgen (queue/done) schon vorkamen, werden ans Ende der Auswahl geschoben.
Keine politisch umstrittenen Flaggen (Kosovo, Taiwan, Palästina, Westsahara, Israel, Russland, Ukraine …)."""
import json, random, sys
from pathlib import Path

AP = Path(__file__).parent
ROOT = AP.parent

LEVELS = {
    'EASY': {'us': 'USA', 'gb': 'United Kingdom', 'fr': 'France', 'de': 'Germany', 'it': 'Italy', 'es': 'Spain', 'jp': 'Japan', 'ca': 'Canada', 'br': 'Brazil', 'cn': 'China', 'in': 'India', 'mx': 'Mexico', 'au': 'Australia', 'kr': 'South Korea', 'ch': 'Switzerland', 'se': 'Sweden', 'tr': 'Turkey', 'gr': 'Greece', 'ar': 'Argentina', 'pt': 'Portugal', 'nl': 'Netherlands', 'za': 'South Africa', 'ie': 'Ireland', 'no': 'Norway', 'eg': 'Egypt', 'jm': 'Jamaica'},
    'MEDIUM': {'be': 'Belgium', 'at': 'Austria', 'pl': 'Poland', 'dk': 'Denmark', 'fi': 'Finland', 'nz': 'New Zealand', 'ng': 'Nigeria', 'ke': 'Kenya', 'sa': 'Saudi Arabia', 'th': 'Thailand', 'vn': 'Vietnam', 'id': 'Indonesia', 'ph': 'Philippines', 'co': 'Colombia', 'cl': 'Chile', 'pe': 'Peru', 'hu': 'Hungary', 'cz': 'Czechia', 'hr': 'Croatia', 'cu': 'Cuba', 'is': 'Iceland', 'ma': 'Morocco', 'pk': 'Pakistan', 'my': 'Malaysia', 'sg': 'Singapore', 'ae': 'UAE'},
    'HARD': {'ee': 'Estonia', 'lv': 'Latvia', 'lt': 'Lithuania', 'sk': 'Slovakia', 'si': 'Slovenia', 'bg': 'Bulgaria', 'ro': 'Romania', 'ba': 'Bosnia', 'al': 'Albania', 'mk': 'North Macedonia', 'ge': 'Georgia', 'am': 'Armenia', 'kz': 'Kazakhstan', 'uz': 'Uzbekistan', 'mn': 'Mongolia', 'np': 'Nepal', 'lk': 'Sri Lanka', 'bd': 'Bangladesh', 'gh': 'Ghana', 'sn': 'Senegal', 'ci': 'Ivory Coast', 'tn': 'Tunisia', 'dz': 'Algeria', 'qa': 'Qatar', 'uy': 'Uruguay', 'py': 'Paraguay', 'bo': 'Bolivia', 'ec': 'Ecuador'},
    'IMPOSSIBLE': {'bt': 'Bhutan', 'sc': 'Seychelles', 'km': 'Comoros', 'kn': 'Saint Kitts and Nevis', 'vc': 'Saint Vincent', 'lc': 'Saint Lucia', 'dm': 'Dominica', 'gd': 'Grenada', 'ki': 'Kiribati', 'tv': 'Tuvalu', 'nr': 'Nauru', 'mh': 'Marshall Islands', 'fm': 'Micronesia', 'pw': 'Palau', 'sb': 'Solomon Islands', 'vu': 'Vanuatu', 'to': 'Tonga', 'ws': 'Samoa', 'tl': 'East Timor', 'er': 'Eritrea', 'dj': 'Djibouti', 'ls': 'Lesotho', 'sz': 'Eswatini', 'bf': 'Burkina Faso', 'cf': 'Central African Rep.', 'gq': 'Equatorial Guinea', 'st': 'São Tomé', 'mr': 'Mauritania'},
}
SPOKEN = {'USA': 'The U S A', 'UAE': 'The U A E', 'Czechia': 'Czechia', 'Central African Rep.': 'Central African Republic', 'São Tomé': 'Sao Tome and Principe', 'Saint Vincent': 'Saint Vincent and the Grenadines', 'Bosnia': 'Bosnia and Herzegovina'}
Q_LINES = ['Which country?', 'Name this flag.', 'What country is this?', 'Do you know this one?', 'Quick!', 'Look closely.', 'Which flag is this?', 'Too easy?', 'Got it?', 'Think fast!']
LEVEL_INTRO = {'EASY': 'Level one. Easy.', 'MEDIUM': 'Level two. Medium.', 'HARD': 'Level three. Hard.', 'IMPOSSIBLE': 'Final level. Impossible!'}


def used_flags():
    used = set()
    for p in (AP / 'queue' / 'done').glob('*.json'):
        try:
            st = json.loads(p.read_text(encoding='utf-8')).get('story', {})
        except Exception:
            continue
        if st.get('type') == 'flagblitz':
            used |= {r['flag'] for r in st.get('rounds', [])}
    return used


def build(sid, per_level=25, seed=None):
    rng = random.Random(seed or sid)
    used = used_flags()
    rounds = []
    for lv, pool in LEVELS.items():
        codes = [c for c in pool if (ROOT / 'public' / 'flags' / f'{c}.svg').exists()]
        rng.shuffle(codes)
        codes.sort(key=lambda c: c in used)  # frische Flaggen zuerst
        for k, c in enumerate(codes[:per_level]):
            q = rng.choice(Q_LINES)
            if k == 0:
                q = f'{LEVEL_INTRO[lv]} {q}'
            name = pool[c]
            rounds.append({'level': lv, 'flag': c, 'name': name, 'lines': {'q': q, 'a': SPOKEN.get(name, name) + '.'}})
    n = len(rounds)
    return {
        'id': sid, 'type': 'flagblitz', 'format': 'long',
        'title': f'Guess the Flag in 3 Seconds – {n} Flags',
        'hookLine': f'Guess the flag in three seconds! {n} flags, from easy to impossible. Keep score, and subscribe for a new flag quiz every day. Let\'s go!',
        'outroLine': f'How many did you get out of {n}? Comment your score, and follow for more flag quizzes!',
        'outroHold': 5.0,
        'timing': {'think': 3.0, 'move': 0.4, 'tail': 0.25},
        'music': 'sfx/game-show.wav', 'musicVolume': 0.06,
        'rounds': rounds,
        'thumbTexts': ['GUESS THE **FLAG**', 'IN **3** SECONDS', 'CAN YOU GET 80?'],
    }


def queue_item(story, date):
    n = len(story['rounds'])
    return {
        'id': story['id'], 'publishAt': '14:00', 'format': 'long',
        'youtube': {
            'title': f'Guess the Flag in 3 Seconds 🌍 {n} Flags – Easy to Impossible',
            'description': (f'Guess the flag in 3 seconds! {n} flags from EASY to IMPOSSIBLE 🌍\n'
                            'Keep score and comment your result 👇\n\nNew flag quiz every day – subscribe!\n\n'
                            '#flagquiz #guesstheflag #geography #quiz #flags\n\nFlag images: flag-icons by Lipis (MIT licence). Music: original.'),
            'tags': ['guess the flag', 'flag quiz', 'guess the flag in 3 seconds', 'flags of the world', 'geography quiz', 'country flags', 'flag quiz easy to impossible', 'quiz'],
            'comment': f'What was your score out of {n}? Which flag got you? 👇',
        },
        'story': story,
    }


if __name__ == '__main__':
    sid, date = sys.argv[1], sys.argv[2]
    per = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 25
    st = build(sid, per)
    if '--demo' in sys.argv:
        (ROOT / 'stories' / f'{sid}.json').write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding='utf-8')
        print('stories/', sid, len(st['rounds']), 'Flaggen')
    else:
        out = AP / 'queue' / f'{date}-{sid}.json'
        out.write_text(json.dumps(queue_item(st, date), indent=1, ensure_ascii=False), encoding='utf-8')
        print(out, len(st['rounds']), 'Flaggen')
