# Plan 2026-11-24

Data (median ~890 views): gaming history wins (tetris 1,932, nintendosony 1,774, gameboy 1,642). Shark short 240 (day 1), space animals (today) 0 – < 48 h.
Retention: "This Bird Collects Blue Objects" held 183 % after 3 s and 94 % at the end (best loop on the channel → animal behaviour keeps viewers even with fewer views); EVERY curve has its steepest drop at 4.5–6.7 s = beat 2 (Hindenburg −14.5 at 4.5 s, Bird −11.4 at 5.1 s).
Competitors: Zack D. Films "The [Thing] That [Unusual Act] + emoji" (AMlsGz_YJD8 8.6M, buxxsDdLtP8 10M). Removed Facts Verse and Simple History (off-niche), added TED-Ed.

## Rules
- Mix: ~70 % gaming / pop-culture history, ~30 % odd true animal stories with Zack-style titles.
- Beat 1 (< 2.5 s): the surprising result first; hookText ≤4 words, all caps.
- Beat 2 (2.5–6 s): a second surprise or a number – NEVER background/date/"in 1980…". Background goes to beat 4+.
- Length 25–35 s, 5–7 beats, each ≤14 words, one "impact": true beat at the twist. Last beat loops back to beat 1.
- Titles: "The [Thing] That [Did Unusual Thing] [emoji] #shorts" or "[Thing] [Did X]. [Payoff]. #shorts". Title case, never slugs.
- B-roll: objects, places, animals only. No celebrity faces. ≥2 sources per story; numbers must match.

## Next 3 episodes
1. pac-man-name – "Pac-Man's First Name Had to Be Changed 🟡 #shorts". Hook "WRONG NAME." Beat 2: "One letter could be scratched into a rude word." Facts: Japan 1980 "Puck Man", renamed Pac-Man for the US. Why: exploit. (written: queue/2026-11-22-pac-man-name.json)
2. nintendo-cards – "Nintendo Is Older Than Cars. It Sold Playing Cards. 🃏 #shorts" (only use "older than cars" phrasing as "Nintendo Was Founded in 1889. It Sold Playing Cards." if unsure). Hook "1889." Beat 2: "Before Mario, before electricity in most homes – cards." Facts: founded 1889 in Kyoto by Fusajiro Yamauchi, hanafuda cards; later taxis, love hotels, instant rice before toys/games (verify each). Why: exploit gaming history.
3. moscow-subway-dogs – "The Stray Dogs That Learned to Ride the Subway 🐕 #shorts". Hook "THEY COMMUTE." Beat 2: "They know which stop is theirs." Facts: some Moscow strays ride the metro (Andrei Poyarkov, A. N. Severtsov Institute). Why: EXPERIMENT animals (bird retention).

## Experiments
- Running: animal stories with "The X That…" titles (shark, space animals, moscow dogs). Stop after 3 below median.
- New (all beats): beat-2 escalation rule – compare 5 s retention vs. old curves.
- Verdict: ancient-history/disaster topics – stopped.

## Do not
- No lowercase/slug titles, no real-person faces, no old-disaster stories, no background in beat 2, no copied Zack D. topics or scripts.

## STRATEGIE 24.11. (Besitzer: „Videos gefallen mir nicht“) – GILT AB SOFORT
- **Kein Wikimedia-B-Roll mehr.** Grund: Laborvideos mit eingebranntem Messtext, Skalenbalken, unscharf, Motiv passt nicht (Sternhimmel bei „lava“).
- **Neuer Look `"look": "motion"`** (src/WildlyTrueMotion.tsx): animierte Grafik, feste Markenpalette, Hook-Text + Motiv ab Frame 0, Wort-Untertitel.
- Jeder Beat braucht statt `broll` ein **`visual`**:
  - `{"type":"hero","emoji":"🦐","label":"Pistol shrimp"}` – großes Motiv
  - `{"type":"number","value":4700,"suffix":"°C","emoji":"🔥","label":"Inside the bubble"}` – Zahl zählt hoch; Jahreszahlen mit `"raw": true`
  - `{"type":"compare","a":{"emoji":"🫧","label":"Shrimp bubble","value":4700},"b":{"emoji":"☀️","label":"Sun surface","value":5500},"unit":"°C"}`
  - `{"type":"emojis","items":["🦐","💨","🐟"],"label":"A jet of water"}` – 2–4 Emojis
  - `{"type":"flag","iso":"jp","label":"Puck Man, 1980"}` – Flagge aus public/flags
  - `{"type":"text","text":"Be nice to crows","emoji":"🐦"}`
- Labels max. ~22 Zeichen. Keine echten Personen, keine Marken-Maskottchen als Bild (nur generische Emojis).
- Produktion ist pausiert (autopilot/wildlytrue/PAUSE), bis der Besitzer den Look freigibt. Alle 4 Queue-Items sind schon umgestellt.
