// Layout "atlas" für normale Quiz-Shorts (Mehrfachauswahl) und VS-Vergleiche – gleicher Druck-Look wie TrueSize.
//   Mehrfachauswahl: große Serifen-Frage, Antworten als gedruckte Liste, richtige Zeile wird mit Tinte gefüllt
//   Vergleich: zwei waagerechte Balken wachsen auf die echten Werte, Überschrift wird zum Gewinner
//   Bild oben nur, wenn es ein echtes Foto/Video gibt (q.image / q.video) – sonst große Ziffer, nie Emoji
import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {QuizQuestion, QuizStory} from './Quiz';
import {A, Grain, Kicker, sans, serif, serifItalic, stripEmoji} from './components/Atlas';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const LETTERS = ['A', 'B', 'C', 'D'];
const X = 64;

const useT = (q: QuizQuestion) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const local = frame / fps;
  return {frame, fps, local, t: q.start + local};
};

/** Frage mit hervorgehobenem **Schlüsselwort** (rot, kursiv, Unterstrich zieht sich, wenn die Stimme es spricht) */
const Marked: React.FC<{text: string; local: number; at?: number}> = ({text, local, at}) => {
  const parts = text.split('**');
  const k = at == null ? 1 : interpolate(local, [at - 0.05, at + 0.3], [0, 1], clamp);
  return (
    <>
      {parts.map((p, i) =>
        i % 2 === 1 ? (
          <span key={i} style={{fontFamily: serifItalic, fontStyle: 'italic', color: A.red, backgroundImage: `linear-gradient(${A.red}, ${A.red})`, backgroundRepeat: 'no-repeat', backgroundPosition: '0 96%', backgroundSize: `${k * 100}% 7px`, paddingBottom: 6}}>
            {p}
          </span>
        ) : (
          <React.Fragment key={i}>{p}</React.Fragment>
        ),
      )}
    </>
  );
};

/** Kleiner Hinweis-Streifen (Hook, "WAIT FOR #6", "FINAL ONE" …) – immer nur einer zur selben Zeit */
const Tag: React.FC<{q: QuizQuestion; index: number; story: QuizStory; local: number}> = ({q, index, story, local}) => {
  const n = story.questions.length;
  const cd = q.countdownStart - q.start;
  const rv = q.reveal - q.start;
  let text = '';
  let from = 0;
  let until = cd;
  let color = A.red;
  if (index === 0 && story.hook && local < 2.8) [text, until] = [story.hook, 2.8];
  else if (index === 0 && story.teaser && local < cd) [text, from, color] = [story.teaser, story.hook ? 2.8 : 0, A.ink];
  else if (index === n - 1 && index > 0 && story.ctaText && local >= rv + 0.5) [text, from, until, color] = [story.ctaText, rv + 0.5, 1e9, A.ink];
  else if (index === n - 1 && index > 0 && story.finalLabel) text = story.finalLabel;
  else if (story.midLabel && index === Math.floor(n / 2) && index !== n - 1) [text, from, color] = [story.midLabel, 0.5, A.ink];
  text = stripEmoji(text);
  if (!text || local < from || local >= until) return null;
  const k = from === 0 && index === 0 ? 1 : interpolate(local, [from, from + 0.25], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  return (
    <div style={{position: 'absolute', left: X, top: 238, opacity: k, transform: `translateX(${(1 - k) * -24}px)`}}>
      <span style={{display: 'inline-block', background: color, color: A.paper, fontFamily: sans, fontWeight: 700, fontSize: 40, letterSpacing: 3, padding: '6px 20px 8px', borderRadius: 6, whiteSpace: 'nowrap'}}>{text.toUpperCase()}</span>
    </div>
  );
};

const Countdown: React.FC<{q: QuizQuestion; t: number; top: number}> = ({q, t, top}) => {
  if (t < q.countdownStart - 0.15 || t >= q.reveal + 0.1) return null;
  const k = interpolate(t, [q.countdownStart, q.reveal], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: X, top, width: 846, height: 8, background: A.grid, borderRadius: 4, overflow: 'hidden'}}>
      <div style={{width: `${k * 100}%`, height: '100%', background: A.ink}} />
    </div>
  );
};

/** Echtes Foto/Video wie ein Abzug im Heft: entsättigt, warm überdruckt, dünner Rand, langsamer Zoom */
const Print: React.FC<{q: QuizQuestion; local: number; revealed: boolean}> = ({q, local, revealed}) => {
  const img = revealed && q.revealImage ? q.revealImage : q.image;
  const zoom = interpolate(local, [0, 10], [1.02, 1.16], clamp);
  const media: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`, filter: 'grayscale(0.85) contrast(1.12) brightness(1.04)'};
  return (
    <div style={{position: 'absolute', left: X, top: 322, width: 952, height: 430, border: `4px solid ${A.ink}`, borderRadius: 6, overflow: 'hidden', boxSizing: 'border-box', background: A.land, transform: 'rotate(-0.6deg)'}}>
      {q.video && !(revealed && q.revealImage) ? <OffthreadVideo src={staticFile(q.video)} muted style={media} /> : img ? <Img src={staticFile(img)} style={media} /> : null}
      <AbsoluteFill style={{background: '#E9C9A0', mixBlendMode: 'multiply', opacity: 0.55}} />
      {revealed && q.revealCaption ? (
        <div style={{position: 'absolute', left: 0, bottom: 0, background: A.ink, color: A.paper, fontFamily: sans, fontWeight: 700, fontSize: 36, letterSpacing: 3, padding: '6px 18px'}}>{stripEmoji(q.revealCaption).toUpperCase()}</div>
      ) : null}
    </div>
  );
};

const Row: React.FC<{q: QuizQuestion; i: number; index: number; y: number; h: number; local: number; t: number; label?: string}> = ({q, i, index, y, h, local, t, label}) => {
  const ok = i === q.correct;
  const since = t - q.reveal;
  const rev = since >= 0;
  const appear = index === 0 ? 1 : interpolate(local, [0.08 + i * 0.07, 0.3 + i * 0.07], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const fill = rev && ok ? interpolate(since, [0, 0.3], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)}) : 0;
  const strike = rev && !ok ? interpolate(since, [0.1 + i * 0.05, 0.4 + i * 0.05], [0, 1], clamp) : 0;
  const check = rev && ok ? interpolate(since, [0.2, 0.55], [0, 1], clamp) : 0;
  const bump = rev && ok ? 1 + 0.03 * Math.sin(Math.min(1, since / 0.5) * Math.PI) : 1;
  const text = stripEmoji(q.answers[i] ?? '') || (q.answers[i] ?? '');
  const size = text.length > 26 ? 42 : text.length > 18 ? 50 : 60;
  const W = 850;
  return (
    <div style={{position: 'absolute', left: 60, top: y, width: W, height: h, opacity: appear * (rev && !ok ? 0.5 : 1), transform: `translateY(${(1 - appear) * 26}px) scale(${bump})`}}>
      <div style={{position: 'absolute', inset: 0, border: `4px solid ${rev && !ok ? A.coast : A.ink}`, borderRadius: 8, background: A.paper, overflow: 'hidden', boxSizing: 'border-box'}}>
        <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${fill * 100}%`, background: A.blue}} />
      </div>
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', padding: '0 28px', gap: 22}}>
        <div style={{fontFamily: serifItalic, fontStyle: 'italic', fontWeight: 900, fontSize: 56, width: 56, color: fill > 0.2 ? A.paper : A.soft, opacity: fill > 0.2 ? 0.75 : 1}}>{LETTERS[i]}</div>
        <div style={{position: 'relative', fontFamily: sans, fontWeight: 600, fontSize: size, letterSpacing: 0.5, color: fill > 0.5 ? A.paper : A.ink, whiteSpace: 'nowrap'}}>
          {text}
          {strike > 0 ? <div style={{position: 'absolute', left: -6, top: '54%', height: 5, width: `calc(${strike * 100}% + 12px)`, background: A.red, borderRadius: 3}} /> : null}
        </div>
      </div>
      {check > 0 ? (
        <svg width={70} height={70} viewBox="0 0 70 70" style={{position: 'absolute', right: 26, top: h / 2 - 35}}>
          <path d="M12 38 L29 54 L59 16" fill="none" stroke={A.paper} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={80} strokeDashoffset={80 * (1 - check)} />
        </svg>
      ) : null}
      {rev && ok && label && since > 0.25 ? (
        <div style={{position: 'absolute', right: 110, top: -22, background: A.ink, color: A.paper, fontFamily: sans, fontWeight: 700, fontSize: 30, letterSpacing: 3, padding: '3px 14px 5px', borderRadius: 4, transform: `rotate(-2deg) scale(${interpolate(since, [0.25, 0.45], [0.6, 1], {...clamp, easing: Easing.out(Easing.back(2))})})`}}>{stripEmoji(label).toUpperCase()}</div>
      ) : null}
    </div>
  );
};

export const AtlasScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const {local, t} = useT(q);
  const revealed = t >= q.reveal;
  const media = Boolean(q.video || q.image);
  const plain = q.q.replace(/\*\*/g, '');
  const qSize = media ? (plain.length > 70 ? 58 : plain.length > 42 ? 70 : 84) : plain.length > 70 ? 74 : plain.length > 42 ? 90 : 106;
  const enter = index === 0 ? 1 : interpolate(local, [0, 0.3], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const n = Math.min(4, q.answers.length);
  const rowH = n <= 2 ? 150 : n === 3 ? 140 : 126;
  const gap = 16;
  const listH = n * rowH + (n - 1) * gap;
  const listY = 1512 - listH;
  // Text ohne Emoji als Rätsel-Fläche (z. B. "2 · 4 · 8 · ?"); reine Emoji-Karten fallen weg
  const puzzle = !media ? stripEmoji(q.cardText) : '';
  const drift = interpolate(local, [0, 12], [0, -26], clamp);
  return (
    <AbsoluteFill style={{background: A.paper}}>
      <Kicker section={story.header} right={`${index + 1}/${total}${q.level ? '  ' + q.level.toUpperCase() : ''}`} />
      {!media ? (
        <div style={{position: 'absolute', right: 34, top: 214 + drift, fontFamily: serifItalic, fontStyle: 'italic', fontWeight: 900, fontSize: 560, lineHeight: 1, color: A.land, opacity: enter}}>{index + 1}</div>
      ) : (
        <div style={{opacity: enter}}>
          <Print q={q} local={local} revealed={revealed} />
        </div>
      )}
      <Tag q={q} index={index} story={story} local={local} />
      <div style={{position: 'absolute', left: X, width: media ? 952 : 880, top: media ? 772 : 326, height: media ? listY - 60 - 772 : listY - 70 - 326, display: 'flex', flexDirection: 'column', justifyContent: media ? 'center' : 'flex-start', opacity: enter, transform: `translateY(${(1 - enter) * 22}px)`}}>
        <div style={{fontFamily: serif, fontWeight: 900, fontSize: qSize, lineHeight: 1.03, letterSpacing: -1.5, color: A.ink}}>
          <Marked text={q.q} local={local} at={q.keywordAt != null ? q.keywordAt - q.start : undefined} />
        </div>
        {puzzle ? <div style={{marginTop: 34, fontFamily: sans, fontWeight: 700, fontSize: 84, letterSpacing: 4, color: A.blue, whiteSpace: 'pre-line'}}>{puzzle}</div> : null}
        {revealed && q.fact ? (
          <div style={{marginTop: 28, fontFamily: sans, fontWeight: 500, fontSize: 42, lineHeight: 1.15, color: A.soft, opacity: interpolate(t - q.reveal, [0.5, 0.9], [0, 1], clamp)}}>{stripEmoji(q.fact)}</div>
        ) : null}
      </div>
      <Countdown q={q} t={t} top={listY - 34} />
      {Array.from({length: n}, (_, i) => (
        <Row key={i} q={q} i={i} index={index} y={listY + i * (rowH + gap)} h={rowH} local={local} t={t} label={story.correctLabel} />
      ))}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------ Vergleich (2 Antworten + values)
const fmtNum = (v: number) => (Math.abs(v) >= 100 ? Math.round(v).toLocaleString('en-US') : String(Math.round(v * 10) / 10));

export const AtlasCompareScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const {frame, local, t} = useT(q);
  const since = t - q.reveal;
  const revealed = since >= 0;
  const vals = q.values ?? [1, 1];
  const max = Math.max(...vals.map(Math.abs), 1e-9);
  const grow = revealed ? interpolate(since, [0, 1.1], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)}) : 0;
  const enter = index === 0 ? 1 : interpolate(local, [0, 0.3], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const pop = interpolate(since, [0.15, 0.5], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.6))});
  const colors = [A.red, A.blue];
  const wName = stripEmoji(q.answers[q.correct]) || q.answers[q.correct];
  const TRACK_W = 952;
  const TRACK_H = 150;
  const ROW_Y = [590, 1010];
  return (
    <AbsoluteFill style={{background: A.paper}}>
      <Kicker section={story.header} right={`${index + 1}/${total}${q.level ? '  ' + q.level.toUpperCase() : ''}`} />
      <Tag q={q} index={index} story={story} local={local} />
      {since < 0.15 ? (
        <div style={{position: 'absolute', left: X, right: X, top: 318, fontFamily: serif, fontWeight: 900, fontSize: 104, lineHeight: 1, letterSpacing: -2, color: A.ink, opacity: enter}}>
          <Marked text={q.q} local={local} at={q.keywordAt != null ? q.keywordAt - q.start : undefined} />
        </div>
      ) : (
        <div style={{position: 'absolute', left: X, right: X, top: 310, fontFamily: serif, fontWeight: 900, fontSize: wName.length > 16 ? 76 : wName.length > 10 ? 96 : 118, lineHeight: 1, letterSpacing: -2, color: colors[q.correct], opacity: Math.min(1, pop * 1.4), transform: `translateY(${(1 - pop) * 24}px)`}}>
          {wName}.
        </div>
      )}
      <Countdown q={q} t={t} top={470} />
      {q.answers.slice(0, 2).map((a, i) => {
        const ok = i === q.correct;
        const y = ROW_Y[i];
        const name = stripEmoji(a) || a;
        const w = Math.max(0.07, Math.abs(vals[i]) / max) * TRACK_W * grow;
        const label = q.valueLabels?.[i] ?? fmtNum(vals[i]);
        const img = q.images?.[i];
        const dim = revealed && !ok ? interpolate(since, [0.6, 1.0], [1, 0.5], clamp) : 1;
        const rowIn = index === 0 ? 1 : interpolate(local, [0.1 + i * 0.1, 0.35 + i * 0.1], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
        return (
          <div key={i} style={{position: 'absolute', left: X, top: y, width: TRACK_W, opacity: rowIn * dim, transform: `translateX(${(1 - rowIn) * 40}px)`}}>
            <div style={{display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', height: 112}}>
              <div style={{fontFamily: sans, fontWeight: 700, fontSize: name.length > 20 ? 62 : 78, lineHeight: 1, letterSpacing: 1.5, color: colors[i], whiteSpace: 'nowrap', paddingBottom: 14}}>{name.toUpperCase()}</div>
              {img ? (
                <div style={{width: 176, height: 104, border: `4px solid ${A.ink}`, borderRadius: 6, overflow: 'hidden', boxSizing: 'border-box', transform: 'rotate(1.2deg)', marginBottom: 8, position: 'relative'}}>
                  <Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'grayscale(0.85) contrast(1.12)', transform: `scale(${interpolate(local, [0, 10], [1.02, 1.18], clamp)})`}} />
                  <AbsoluteFill style={{background: '#E9C9A0', mixBlendMode: 'multiply', opacity: 0.55}} />
                </div>
              ) : null}
            </div>
            <svg width={TRACK_W} height={TRACK_H} style={{display: 'block', overflow: 'visible'}}>
              <defs>
                <pattern id={`hatch${index}${i}`} width={22} height={22} patternUnits="userSpaceOnUse" patternTransform={`rotate(35) translate(${(frame * 0.5) % 22} 0)`}>
                  <rect width={22} height={22} fill={colors[i]} />
                  <rect width={3} height={22} fill="rgba(255,255,255,0.16)" />
                </pattern>
              </defs>
              {!revealed ? (
                <rect x={2} y={2} width={TRACK_W - 4} height={TRACK_H - 4} rx={8} fill="none" stroke={A.coast} strokeWidth={4} strokeDasharray="16 12" strokeDashoffset={-frame * 0.6} />
              ) : (
                <>
                  <rect x={2} y={2} width={TRACK_W - 4} height={TRACK_H - 4} rx={8} fill="none" stroke={A.grid} strokeWidth={4} />
                  <rect x={0} y={0} width={Math.max(10, w)} height={TRACK_H} rx={8} fill={`url(#hatch${index}${i})`} />
                </>
              )}
            </svg>
            <div style={{height: 84, display: 'flex', alignItems: 'center', fontFamily: serif, fontWeight: 900, fontSize: 60, letterSpacing: -1, color: revealed ? A.ink : A.coast}}>
              {revealed ? <span style={{opacity: interpolate(since, [0.3, 0.7], [0, 1], clamp)}}>{label}</span> : <span style={{fontFamily: serifItalic, fontStyle: 'italic', transform: `scale(${1 + 0.05 * Math.sin(local * 4 + i)})`, display: 'inline-block'}}>?</span>}
              {revealed && ok && since > 0.7 && story.correctLabel ? (
                <span style={{marginLeft: 22, background: A.ink, color: A.paper, fontFamily: sans, fontWeight: 700, fontSize: 32, letterSpacing: 3, padding: '3px 14px 5px', borderRadius: 4, transform: `scale(${interpolate(since, [0.7, 0.9], [0.6, 1], {...clamp, easing: Easing.out(Easing.back(2))})})`}}>{stripEmoji(story.correctLabel).toUpperCase()}</span>
              ) : null}
            </div>
          </div>
        );
      })}
      <div style={{position: 'absolute', left: X, top: ROW_Y[1] - 66, fontFamily: serifItalic, fontStyle: 'italic', fontWeight: 900, fontSize: 54, color: A.coast, opacity: enter}}>or</div>
    </AbsoluteFill>
  );
};

export const AtlasOutro: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const k = interpolate(frame / fps, [0, 0.35], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  return (
    <AbsoluteFill style={{background: A.paper}}>
      <Kicker section={story.header} />
      <div style={{position: 'absolute', left: X, right: X, top: 420, opacity: k, transform: `translateY(${(1 - k) * 24}px)`}}>
        <div style={{fontFamily: serif, fontWeight: 900, fontSize: 118, lineHeight: 1, letterSpacing: -2, color: A.ink}}>{stripEmoji(story.outroText)}</div>
        <div style={{marginTop: 40, fontFamily: serifItalic, fontStyle: 'italic', fontWeight: 900, fontSize: 300, lineHeight: 1, color: A.red}}>?/{story.questions.length}</div>
        {story.outroSub ? <div style={{marginTop: 30, fontFamily: sans, fontWeight: 600, fontSize: 54, letterSpacing: 1, color: A.ink}}>{stripEmoji(story.outroSub)}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

export const AtlasGrain = Grain;
