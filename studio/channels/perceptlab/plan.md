# Plan 2026-11-26

Data: Afterimage flag "Stare at This Flag for 20 Seconds…" 1,393 views after 2 days (was 592 on day 1) = best new short, back at old-winner level (Spiral 1,274 / Dot 1,098). Müller-Lyer 6 (stopped). Ebbinghaus "Brain Test #1" + Blind spot not live long enough for a verdict.
Cause: the viewer DOES something for 20 s and gets a personal payoff (colours appear) → "stare, then look" afterimage = EXPLOIT (1 of 3 shorts). Static comparisons remain stopped.
Competitors: Dramatic_science spin illusions 3j_BH1oT_SE (13×, 1.3M) + 5 more at 3.3–3.7×; MindWarp 3D ZP4wjmfjSw0 (5.3×) = full-screen black/white op-art rings with ONE red centre dot (thumbnail checked) → used for the spin + stare formats.

## Rules
- Every short is a TEST the viewer does: line 1 = instruction or question to "you". Never open with a fact or a name.
- Something MOVES from frame 0 (rotation, pulsing rings, zoom). No static line/bar comparisons any more.
- Line 2 (2.5–6 s) raises the stakes ("Now make it spin the other way. Only with your mind."), never an explanation. Visual change at ~4.5 s.
- Length 15–30 s, max ~60 words. Reveal ~60 %, explanation max 2 lines, last line loops ("Now look again.").
- Titles: "[Instruction/question to you] + [challenge] + emoji #shorts". Series "Brain Test #N" in the description (not required in title).
- Style: dark/black background, neon or white dots/lines, object large and centred (competitor look) OR chalkboard lab; high contrast.
- ANIMATION TRICK (engine supports it): paint 16–24 stages of one plate (e.g. a sphere of dots rotated by 360/N degrees each, orthographic projection, NO size/brightness depth cues = ambiguous direction) and cycle them with a long `show` list, e.g. show=[(i/12, i % 24) for i in range(12*30)] → 12 fps rotation loop. Camera static (slow push max). Keep N ≤ 24 (memory).
- Fact (illusion name + year) only in the last 1–2 lines; all facts verified.

## Next 3 episodes (after 005-spin-sphere)
1. 006-tickle – "Why Can't You Tickle Yourself? Try It 🧠 #shorts" (cerebellum predicts own touch, Blakemore/Wolpert/Frith 1998–2000). (written: 006-tickle) Why: experiment "Why can't you…?" (SciShow pattern). Hook starts with the instruction: "Try to tickle yourself. Right now."
2. 007-see-first-1 – "What Did You See First? 👇 #1 #shorts" (10–14 s, 3–4 lines). Hook: "What did you see first? Don't think." L2: "Look again. There are two." Reveal: "A vase – or two faces. Your brain can't see both at once." Last: "Comment what you saw first." Own drawing of a Rubin vase in neon on black. Why: vidIQ outlier (ambiguous figures 1.6–4.2M).
3. 008-afterimage-photo – EXPLOIT (afterimage #2): "Stare for 20 Seconds. This Black & White Photo Turns Colour 👁️ #shorts". Hook: "Stare at the red dot. Don't move your eyes." L2: "Twenty seconds. These colours look wrong on purpose." Countdown card 20→0, then cut to the SAME scene in plain grey/black & white: "Now – it's in colour. Isn't it?" Explanation (1 line): "Your colour cells got tired. Your brain paints the opposite." Last: "Blink, and it's gone. Watch again." Visual: own painted simple landscape (sky, sun, grass, red barn) – plate A = colour-INVERTED version (PIL ImageOps.invert: blue sky→yellow, green→magenta), white/red dot centred; plate B = grayscale of the normal painting (ImageOps.grayscale), same dot. Hold plate A still ≥ 20 s (no camera move!), hard cut to plate B. Why: exploit of 002 (1,393), one variable changed (photo instead of flag).

## Experiments
- EXPLOIT: afterimage "stare 20 s, then look" (002 ✔ 1,393) – repeat as #2 (008); if ≥ 1,000 again, make it a weekly series "Stare Test #N".
- Running: "Brain Test #N" (003 Ebbinghaus). Spin/motion tests (005) new. Ultra-short ambiguous figures (007) new. Verdict each after 7 days; stop a type after 3 below median (~1,000).
- Verdicts: static length comparisons STOPPED (Müller-Lyer 6 views; Ponzo dropped). Probability paradoxes paused. Opinion topics stopped.

## Do not
- No static two-line/bar comparisons, no slow openings, no opinion/spiritual topics, no invented statistics or fake poll percentages, no explanations > 2 lines, no real-person likeness, no copying competitor visuals 1:1 (own colours, own wording).
