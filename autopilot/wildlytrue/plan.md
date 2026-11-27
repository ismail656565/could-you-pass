# Plan 2026-11-27

Data (median ~890): gaming history still best (tetris 1,932, nintendosony 1,774, gameboy 1,642). Greenland shark 388 (43 % stayed), space animals 175 – single-animal stories below median. Production PAUSED (owner reviewing the new motion look) – plan stays ready.
Retention: every curve loses most at 4.5–6.7 s = beat 2.
Status 27.11.: still PAUSED, no new uploads; plan unchanged and ready. New competitor signal: The Wildest Dose dP0-jKtFhzY "What is THAT?!" (19.9×, 1.27M) and E. FRANK fSIlQncWQ2k "5 Animals That Actually Hunt Humans" (9.8×) – thumbnail checked: real animal face (shoebill) huge, centred, one-word label ("HUMAN") → hero visual with one-word label from frame 0.
Competitors: E. FRANK iykYjcSycNg "5 Extinct Animals Scientists Are Bringing Back 😨" (28×, 8.6M), j7MMYEKv9g4 (17×), 3CRpIIT5Uvs (14×) = LIST of 5 with one huge animal close-up per item; The Wildest Dose dP0-jKtFhzY "What is THAT?!" (18×) = one bizarre creature on plain background (thumbnail checked).

## Rules
- Mix: ~60 % gaming / pop-culture history (proven), ~40 % animal LISTS "5 Animals That…" (new, competitor-proven) – single animal stories only if the claim is extreme.
- Beat 1 (< 2.5 s): the surprising result / list promise ("Number five breathes through its butt."), hookText ≤ 4 words, all caps.
- Beat 2 (2.5–6 s): first item or a second surprise with a number – NEVER background/date.
- Lists: 5 items, 1 beat each (≤ 12 words), count DOWN 5→1, best item last, each beat a `hero` visual with emoji + label ≤ 22 chars; 30–40 s.
- Single stories: 25–35 s, 5–7 beats ≤ 14 words, one "impact": true at the twist, last beat loops.
- Titles: "5 Animals That [Shock Claim] [😱/😨] #shorts" or "The [Thing] That [Did Unusual Thing] [emoji] #shorts". Title case, never slugs.
- Visuals only via the motion look (see below). ≥ 2 sources per fact, numbers must match.

## Next 3 episodes
1. 5-butt-breathers – "5 Animals That Breathe Through Their Butts 😳 #shorts". Items (verify each, 2 sources): Fitzroy River turtle (cloacal respiration), sea cucumber (respiratory trees via cloaca), dragonfly nymph (rectal gills), weather loach (swallows air, intestinal breathing, gas out the vent), and #1 mammals: 2021 study (Takebe lab, Tokyo/Cincinnati) – mice and pigs absorbed oxygen through the rectum (lab only). Hook "BUTT BREATHERS." Why: EXPERIMENT list format, competitor j7MMYEKv9g4 (own topic).
2. nintendo-cards – "Nintendo Was Founded in 1889. It Sold Playing Cards. 🃏 #shorts". Hook "1889." Beat 2: "Before Mario – hand-painted cards." Facts: Fusajiro Yamauchi, Kyoto, hanafuda; later taxi company, love hotels, instant rice (verify each). Why: EXPLOIT gaming history.
3. moscow-subway-dogs – "The Stray Dogs That Ride the Subway to Work 🐕 #shorts". Hook "THEY COMMUTE." Beat 2: "They know which stop is theirs." Facts: Moscow metro strays (Andrei Poyarkov, Severtsov Institute). Why: animal behaviour (bird-loop retention); last single-animal test – stop single animal stories if it lands below median.

## Experiments
- Animal "The X That…" singles: shark 385, space animals 172 → 2 of 3 below median; moscow dogs is the third and decides.
- New: "5 Animals That…" lists – verdict after 3.
- Stopped: ancient-history/disaster topics.

## Do not
- No lowercase/slug titles, no real-person faces, no old-disaster stories, no background in beat 2, no copied E. FRANK/Zack D. lists (no "without sleep", "bringing back", "hybrids", "hunt humans", "immortal").

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
