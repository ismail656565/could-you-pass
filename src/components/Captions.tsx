import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {CaptionWord} from '../types';
import {isEmphasis, theme} from '../theme';


type Chunk = {words: CaptionWord[]; start: number; end: number};

// Wörter zu kurzen Häppchen (max. 3 Wörter) gruppieren; Satzzeichen beenden ein Häppchen
const toChunks = (words: CaptionWord[], maxWords: number): Chunk[] => {
  const chunks: Chunk[] = [];
  let current: CaptionWord[] = [];
  const flush = () => {
    if (current.length === 0) return;
    chunks.push({words: current, start: current[0].start, end: current[current.length - 1].end});
    current = [];
  };
  for (const w of words) {
    current.push(w);
    const endsSentence = /[.!?,;:—–]$/.test(w.word.trim());
    if (current.length >= maxWords || endsSentence) flush();
  }
  flush();
  // Häppchen bis zum nächsten verlängern, damit kein Flackern zwischen ihnen entsteht
  for (let i = 0; i < chunks.length - 1; i++) {
    const gap = chunks[i + 1].start - chunks[i].end;
    if (gap > 0 && gap < 0.6) chunks[i].end = chunks[i + 1].start;
  }
  return chunks;
};

// Fallback ohne Whisper: Skriptwörter gleichmäßig über die Sprechzeit verteilen (nur für Vorschauen)
export const estimateWords = (script: string, from: number, to: number): CaptionWord[] => {
  const tokens = script.split(/\s+/).filter(Boolean);
  if (tokens.length === 0) return [];
  // Längere Wörter bekommen etwas mehr Zeit
  const weights = tokens.map((t) => 1 + t.length * 0.12 + (/[.!?]$/.test(t) ? 1.2 : 0));
  const total = weights.reduce((a, b) => a + b, 0);
  const span = to - from;
  let t = from;
  return tokens.map((word, i) => {
    const d = (weights[i] / total) * span;
    const w = {word, start: t, end: t + d * 0.92};
    t += d;
    return w;
  });
};


export const Captions: React.FC<{words: CaptionWord[]; energy?: 'normal' | 'high' | 'clean'; retro?: boolean; sport?: boolean; space?: boolean}> = ({
  words,
  energy = 'normal',
  retro = false,
  sport = false,
  space = false,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const high = energy === 'high';
  const clean = energy === 'clean';
  const chunks = useMemo(() => {
    const c = toChunks(words, high || clean ? 2 : 3);
    // Im ruhigen Modus steht der erste Untertitel schon im allerersten Frame
    if (clean && c.length && c[0].start < 0.5) c[0] = {...c[0], start: 0};
    return c;
  }, [words, high, clean]);

  const chunk = chunks.find((c) => t >= c.start && t < c.end);
  if (!chunk) return null;

  const chunkStartFrame = Math.round(chunk.start * fps);
  const pop = spring({
    frame: frame - chunkStartFrame,
    fps,
    config: high ? {damping: 10, stiffness: 320, mass: 0.5} : {damping: 14, stiffness: 220, mass: 0.6},
  });
  const chunkIndex = chunks.indexOf(chunk);
  // ruhig: kaum Aufpoppen, erster Untertitel steht sofort voll da
  const popFrom = clean ? (chunkIndex === 0 ? 1 : 0.92) : high ? 0.55 : 0.82;
  const scale = interpolate(pop, [0, 1], [popFrom, 1]);
  const y = interpolate(pop, [0, 1], [clean ? (chunkIndex === 0 ? 0 : 10) : high ? 40 : 24, 0]);
  const tilt = high ? (chunkIndex % 2 === 0 ? -2.5 : 2.5) * (1 - pop) + (chunkIndex % 2 === 0 ? -1 : 1) : 0;
  const hi = retro ? theme.cyan : sport ? theme.pitch : space ? theme.hud : theme.yellow;
  const hot = retro ? theme.magenta : space ? theme.nasaOrange : theme.yellow;

  return (
    <AbsoluteFill style={{alignItems: 'center'}}>
      <div
        style={{
          position: 'absolute',
          top: theme.captionY,
          width: 960,
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '0 22px',
          transform: `translateY(${y}px) scale(${scale}) rotate(${tilt}deg)`,
        }}
      >
        {chunk.words.map((w, i) => {
          const active = t >= w.start && t < w.end + 0.05;
          const spoken = t >= w.start;
          const color = isEmphasis(w.word) ? hot : active ? hi : theme.white;
          return (
            <span
              key={`${w.start}-${i}`}
              style={{
                fontFamily: retro ? theme.pixel : theme.display,
                fontSize: retro ? 70 : high ? 132 : clean ? 124 : 118,
                lineHeight: retro ? 1.35 : 1.08,
                textTransform: 'uppercase',
                color,
                opacity: spoken ? 1 : 0.55,
                WebkitTextStroke: retro ? '6px black' : '7px black',
                paintOrder: 'stroke fill',
                textShadow: retro
                  ? `5px 5px 0 ${theme.black}, 0 0 28px ${color}88`
                  : space
                    ? `0 0 26px ${color}99, 0 8px 24px rgba(0,0,0,0.6)`
                    : '0 8px 24px rgba(0,0,0,0.6)',
                transform: active ? 'scale(1.08)' : 'scale(1)',
                display: 'inline-block',
              }}
            >
              {w.word.replace(/[,;]$/, '')}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
