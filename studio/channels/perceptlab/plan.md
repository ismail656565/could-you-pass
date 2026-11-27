# Plan 2026-11-27

Data (median ~1,000): afterimage flag "Stare at This Flag for 20 Seconds…" 1,394 (59.7 % stayed) = best short. "Which Orange Circle Is Bigger? Brain Test #1" (Ebbinghaus) only 53 after 1.5 days = SECOND static size-comparison flop (after Müller-Lyer 6).
Cause: static "which is bigger/longer" = no action, no motion, classic everyone knows → swiped. Winners: viewer DOES something (stare 20 s, close an eye) + personal payoff. Blind spot (27.11.) + spin sphere (28.11.) not live long enough.
Competitors: Dramatic_science 3j_BH1oT_SE "Can you reverse the spin…" (13×, 1.3M) + 5 spin variants 3.3–3.7×; MindWarp 3D Z3GmTopETSA/ZP4wjmfjSw0 (4.8–5.3×) = full-screen pulsing op-art rings (black/white + red/yellow), ONE red dot centre, title "This … Will Trick Your Brain" (thumbnails checked).

## Rules
- Every short is a TEST the viewer does: line 1 = instruction or question to "you". Never open with a fact or a name.
- Something MOVES from frame 0 (rotation, pulsing rings, zoom). Static comparisons are BANNED (Brain Test #1 = 53 views).
- Line 2 (2.5–6 s) raises the stakes, never an explanation. Visual change at ~4.5 s.
- Length 15–30 s, max ~60 words. Reveal ~60 %, explanation max 2 lines, last line loops ("Now look again.").
- Titles: "[Instruction to you] + [payoff] + emoji #shorts" (e.g. "Stare at the Red Dot for 20 Seconds…"). Series name in description ("Stare Test #N", "Spin Test #N").
- Style: black background, high-contrast neon/white op-art, object large and centred; red fixation dot.
- ANIMATION TRICK (engine supports it): paint 16–24 stages of one plate and cycle them with a long `show` list, e.g. show=[(i/12, i % 24) for i in range(12*30)] → 12 fps loop. Camera static. N ≤ 24.
- Fact (illusion name + year) only in the last 1–2 lines; all facts verified.

## Next 3 episodes (after 006-tickle, already written)
1. 007-afterimage-photo – EXPLOIT (Stare Test #2): "Stare for 20 Seconds. This Black & White Photo Turns Colour 👁️ #shorts". Hook: "Stare at the red dot. Don't move your eyes." L2: "Twenty seconds. These colours look wrong on purpose." Countdown card 20→0, hard cut to the SAME scene in grayscale: "Now – it's in colour. Isn't it?" Explain (1 line): "Your colour cells got tired. Your brain paints the opposite." Last: "Blink, and it's gone. Watch again." Visual: own painted landscape (sky, sun, grass, red barn); plate A = ImageOps.invert of the painting + red dot centred, held still ≥ 20 s; plate B = ImageOps.grayscale of the normal painting, same dot. Why: exploit of 002 (1,394). (written: 007-afterimage-photo)
2. 008-pulse-rings – EXPERIMENT (competitor MindWarp ZP4wjmfjSw0 pattern, own design): "Stare at the Red Dot. The Rings Will Start to Breathe 🌀 #shorts". Hook: "Stare at the red dot. Only the dot." L2: "Ten seconds. Now the rings start moving – but nothing moves." Visual: 24 plate stages of concentric black/white rings with a tiny phase shift each (cycled = pulsing), then from ~10 s a STILL plate (static rings) – viewers see motion anyway (motion aftereffect / peripheral drift). Reveal: "That last picture was a still image." Explain: "Your motion cells got tired and now fire the other way." Last: "Scroll back. Watch it again." Why: competitor 4.8–5.3× + stare exploit.
3. 009-spin-2 – only if 005-spin-sphere ≥ 800 views by 30.11.: "Can You Make the Dancer Dots Spin the Other Way? Spin Test #2 🧠 #shorts" (ring of dots instead of sphere, same 24-stage trick). Otherwise: 009 = "What Did You See First? 👇 #1" (own neon Rubin vase, 10–14 s, 4 lines, last line "Comment what you saw first.").

## Experiments
- EXPLOIT: Stare Test (afterimage) – #2 = 007; if ≥ 1,000 → weekly series.
- Running: blind spot (004), spin (005), tickle "Why can't you…" (006) – verdict 7 days after publish, stop a type after 3 below ~1,000.
- New: pulsing-ring stare (008).
- STOPPED: static size/length comparisons (Müller-Lyer 6, Ebbinghaus 53), probability paradoxes, opinion topics.

## Do not
- No static comparisons, no slow openings, no explanations > 2 lines, no invented statistics, no real-person likeness, no 1:1 copies of competitor visuals (own colours/geometry, own wording).
