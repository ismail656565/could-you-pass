import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Story} from './types';
import {Captions, estimateWords} from './components/Captions';
import {HOOK_SECONDS, HookCard} from './components/HookCard';
import {theme} from './theme';

/**
 * WILDLY TRUE – Look "motion": animierte Grafik statt Fremd-Footage.
 * Jeder Beat hat ein "visual" (hero | number | compare | emojis | flag | text).
 * Frame 0 zeigt schon das Motiv von Beat 1 + den Hook-Text.
 */

export type MotionVisual =
  | {type: 'hero'; emoji: string; label?: string}
  | {type: 'number'; value: number; prefix?: string; suffix?: string; label?: string; emoji?: string; decimals?: number; /** Jahreszahl: ohne Tausenderpunkt */ raw?: boolean}
  | {type: 'compare'; a: {emoji: string; label: string; value: number}; b: {emoji: string; label: string; value: number}; unit?: string}
  | {type: 'emojis'; items: string[]; label?: string}
  | {type: 'flag'; iso: string; label?: string}
  | {type: 'text'; text: string; emoji?: string};

export type MotionScene = {start: number; end: number; visual?: MotionVisual};
export type MotionStory = Omit<Story, 'scenes'> & {scenes: MotionScene[]};

// feste Markenpalette: [Hintergrund oben, unten, Akzent]
const PALETTE: [string, string, string][] = [
  ['#1B0F2E', '#4A1030', theme.red],
  ['#0B1D33', '#123E5C', theme.yellow],
  ['#21102A', '#5B1B1B', '#FF8A00'],
  ['#0E2420', '#14463A', theme.yellow],
];

const EMOJI_FONT = '"Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", sans-serif';
const fmt = (v: number, d = 0, raw = false) => v.toLocaleString('en-US', {minimumFractionDigits: d, maximumFractionDigits: d, useGrouping: !raw});

const Background: React.FC<{idx: number; t: number}> = ({idx, t}) => {
  const [top, bottom, accent] = PALETTE[idx % PALETTE.length];
  const blobs = [0, 1, 2].map((i) => ({
    x: 540 + Math.sin(t * 0.35 + i * 2.1) * 380,
    y: 500 + i * 520 + Math.cos(t * 0.28 + i * 1.3) * 160,
    r: 420 - i * 60,
  }));
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${top} 0%, ${bottom} 100%)`}}>
      {blobs.map((b, i) => (
        <div key={i} style={{position: 'absolute', left: b.x - b.r, top: b.y - b.r, width: b.r * 2, height: b.r * 2, borderRadius: '50%',
          background: `radial-gradient(circle, ${i === 0 ? accent : '#ffffff'}${i === 0 ? '33' : '10'} 0%, transparent 70%)`}} />
      ))}
      {/* feines Punktraster, langsam nach oben */}
      <AbsoluteFill style={{opacity: 0.12, backgroundImage: 'radial-gradient(#ffffff 1.6px, transparent 1.6px)', backgroundSize: '44px 44px',
        backgroundPosition: `0px ${-(t * 18) % 44}px`}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};

const Label: React.FC<{text?: string; color: string; delay?: number}> = ({text, color, delay = 4}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!text) return null;
  const p = spring({frame: frame - delay, fps, config: {damping: 14, stiffness: 180}});
  return (
    <div style={{marginTop: 26, fontFamily: theme.display, fontSize: 66, color: theme.white, textTransform: 'uppercase', letterSpacing: 2,
      background: color === theme.yellow ? '#00000066' : '#00000055', borderBottom: `8px solid ${color}`, padding: '6px 26px 2px',
      transform: `translateY(${(1 - p) * 40}px)`, opacity: p, textAlign: 'center', maxWidth: 940}}>
      {text}
    </div>
  );
};

const Glow: React.FC<{color: string; size: number}> = ({color, size}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{position: 'absolute', width: size, height: size, borderRadius: '50%', border: `6px solid ${color}`,
      opacity: 0.35 + 0.15 * Math.sin(frame / 6), transform: `scale(${1 + 0.04 * Math.sin(frame / 9)}) rotate(${frame}deg)`,
      borderStyle: 'dashed'}} />
  );
};

const Emoji: React.FC<{e: string; size: number; float?: boolean}> = ({e, size, float = true}) => {
  const frame = useCurrentFrame();
  const y = float ? Math.sin(frame / 14) * 14 : 0;
  const r = float ? Math.sin(frame / 22) * 4 : 0;
  return <div style={{fontFamily: EMOJI_FONT, fontSize: size, lineHeight: 1, transform: `translateY(${y}px) rotate(${r}deg)`,
    filter: 'drop-shadow(0 24px 30px rgba(0,0,0,0.45))'}}>{e}</div>;
};

const Visual: React.FC<{v: MotionVisual; accent: string; dur: number}> = ({v, accent, dur}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const center: React.CSSProperties = {display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'};
  if (v.type === 'hero') {
    return (
      <div style={center}>
        <div style={{...center, width: 470, height: 470}}>
          <Glow color={accent} size={470} />
          <Emoji e={v.emoji} size={290} />
        </div>
        <Label text={v.label} color={accent} />
      </div>
    );
  }
  if (v.type === 'number') {
    const p = interpolate(frame, [0, Math.min(dur * fps * 0.6, 45)], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
    const done = p >= 1;
    const punch = done ? spring({frame: frame - Math.min(dur * fps * 0.6, 45), fps, config: {damping: 8, stiffness: 260}}) : 0;
    const text = `${v.prefix ?? ''}${fmt(v.raw ? Math.round(v.value - (1 - p) * 60) : v.value * p, v.decimals ?? 0, v.raw)}${v.suffix ?? ''}`;
    const size = Math.min(230, Math.floor(1700 / Math.max(4, text.length)));
    return (
      <div style={center}>
        {v.emoji ? <Emoji e={v.emoji} size={150} /> : null}
        <div style={{fontFamily: theme.display, fontSize: size, color: accent, lineHeight: 1, marginTop: 20,
          WebkitTextStroke: '10px #000', paintOrder: 'stroke fill', transform: `scale(${1 + punch * 0.06})`,
          textShadow: '0 16px 0 rgba(0,0,0,0.35)'}}>{text}</div>
        <Label text={v.label} color={accent} delay={8} />
      </div>
    );
  }
  if (v.type === 'compare') {
    const max = Math.max(v.a.value, v.b.value) || 1;
    const grow = (d: number) => interpolate(frame, [d, d + 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
    const side = (s: {emoji: string; label: string; value: number}, d: number, color: string) => {
      const g = grow(d);
      return (
        <div style={{...center, width: 420, justifyContent: 'flex-end', height: 600}}>
          <div style={{fontFamily: theme.display, fontSize: 70, color: theme.white, WebkitTextStroke: '6px #000', paintOrder: 'stroke fill', opacity: g}}>
            {fmt(s.value * g)}{v.unit ? ` ${v.unit}` : ''}
          </div>
          <div style={{width: 220, height: 320 * (s.value / max) * g + 8, background: color, borderRadius: '18px 18px 0 0', marginTop: 12,
            boxShadow: `0 0 50px ${color}88`}} />
          <Emoji e={s.emoji} size={110} float={false} />
          <div style={{fontFamily: theme.display, fontSize: 46, color: theme.white, textAlign: 'center', textTransform: 'uppercase', marginTop: 8}}>{s.label}</div>
        </div>
      );
    };
    return <div style={{display: 'flex', gap: 60, alignItems: 'flex-end'}}>{side(v.a, 0, theme.white)}{side(v.b, 10, accent)}</div>;
  }
  if (v.type === 'emojis') {
    return (
      <div style={center}>
        <div style={{display: 'flex', gap: 40, flexWrap: 'wrap', justifyContent: 'center', maxWidth: 980}}>
          {v.items.slice(0, 4).map((e, i) => {
            const p = spring({frame: frame - i * 7, fps, config: {damping: 10, stiffness: 200}});
            return <div key={i} style={{transform: `scale(${p}) rotate(${(1 - p) * -30}deg)`}}><Emoji e={e} size={v.items.length > 2 ? 210 : 260} /></div>;
          })}
        </div>
        <Label text={v.label} color={accent} delay={v.items.length * 7} />
      </div>
    );
  }
  if (v.type === 'flag') {
    return (
      <div style={center}>
        <div style={{width: 640, height: 480, borderRadius: 24, overflow: 'hidden', border: '10px solid #fff', boxShadow: '0 30px 60px rgba(0,0,0,0.5)',
          transform: `rotate(${Math.sin(frame / 18) * 3}deg)`}}>
          <Img src={staticFile(`flags/${v.iso}.svg`)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
        <Label text={v.label} color={accent} />
      </div>
    );
  }
  // text
  return (
    <div style={center}>
      {v.emoji ? <Emoji e={v.emoji} size={220} /> : null}
      <div style={{fontFamily: theme.display, fontSize: 120, color: theme.white, textAlign: 'center', textTransform: 'uppercase', lineHeight: 1,
        maxWidth: 960, WebkitTextStroke: '9px #000', paintOrder: 'stroke fill', marginTop: 20}}>{v.text}</div>
    </div>
  );
};

const SceneView: React.FC<{scene: MotionScene; idx: number; dur: number; first: boolean}> = ({scene, idx, dur, first}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const accent = PALETTE[idx % PALETTE.length][2];
  // Frame 0 des Videos: voll sichtbar (kein Einblenden), sonst Pop-in mit kleinem Dreh
  const enter = first ? 1 : spring({frame, fps, config: {damping: 13, stiffness: 190}});
  const exitStart = dur * fps - 5;
  const exit = interpolate(frame, [exitStart, exitStart + 5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dir = idx % 2 === 0 ? 1 : -1;
  const v = scene.visual ?? {type: 'text', text: ''};
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingBottom: 260}}>
      <div style={{transform: `translateX(${(1 - enter) * 300 * dir - exit * 200 * dir}px) scale(${0.7 + 0.3 * enter - exit * 0.15}) rotate(${(1 - enter) * 8 * dir}deg)`,
        opacity: 1 - exit * 0.6}}>
        <Visual v={v} accent={accent} dur={dur} />
      </div>
    </AbsoluteFill>
  );
};

const Flash: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 4], [0.5, 0], {extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{background: '#fff', opacity: o}} />;
};

export const WildlyTrueMotion: React.FC<MotionStory> = (story) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const t = frame / fps;
  const f = (s: number) => Math.round(s * fps);
  const words = useMemo(
    () => (story.captions && story.captions.length > 0 ? story.captions : estimateWords(story.script, 0.1, story.durationInSeconds - 0.2)),
    [story.captions, story.script, story.durationInSeconds],
  );
  const scenes = story.scenes;
  let idx = scenes.findIndex((s) => t < s.end);
  if (idx < 0) idx = scenes.length - 1;
  const hook = story.hookText;

  return (
    <AbsoluteFill style={{backgroundColor: theme.black, overflow: 'hidden'}}>
      <Background idx={idx} t={t} />
      {scenes.map((s, i) => (
        <Sequence key={i} from={f(s.start)} durationInFrames={Math.max(1, f(s.end) - f(s.start))} name={`Beat ${i + 1} (${s.visual?.type ?? '-'})`}>
          <SceneView scene={s} idx={i} dur={s.end - s.start} first={i === 0} />
          {i > 0 ? <Flash /> : null}
        </Sequence>
      ))}

      {/* Hook-Text oben ab Frame 0, danach Untertitel */}
      <Sequence durationInFrames={Math.max(1, durationInFrames)} name="Untertitel">
        <Captions words={hook ? words.filter((w) => w.end > HOOK_SECONDS - 0.2) : words} energy="normal" />
      </Sequence>
      {hook ? (
        <Sequence durationInFrames={f(HOOK_SECONDS)} name="Hook-Text">
          <HookCard text={hook} retro={false} />
        </Sequence>
      ) : null}

      {/* Fortschritt + Marke */}
      <div style={{position: 'absolute', left: 0, top: 0, height: 12, width: `${(frame / durationInFrames) * 100}%`, background: theme.yellow}} />
      <div style={{position: 'absolute', right: 48, top: 150, opacity: interpolate(frame, [45, 60], [0, 0.85], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        transform: 'rotate(-6deg)', border: `4px solid ${theme.red}`, borderRadius: 6, padding: '4px 12px 0', color: theme.red,
        fontFamily: theme.display, fontSize: 38, letterSpacing: 2}}>{story.brand ?? 'WILDLY TRUE'}</div>
      {/* kleine Partikel für Bewegung im Bild */}
      {[...Array(14)].map((_, i) => {
        const x = random(`px-${i}`) * 1080;
        const sp = 20 + random(`ps-${i}`) * 40;
        const y = 1920 - ((t * sp + random(`py-${i}`) * 1920) % 2000);
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: 6, height: 6, borderRadius: 3, background: '#ffffff', opacity: 0.25}} />;
      })}

      {story.audio ? <Audio src={staticFile(story.audio)} /> : null}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.1} loop /> : null}
    </AbsoluteFill>
  );
};
