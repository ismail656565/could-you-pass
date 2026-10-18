import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, random, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {CaptionWord, Scene} from '../types';
import {isEmphasis, theme} from '../theme';

/** Zeitpunkte (Sekunden) der Betonungs-Wörter, mit Mindestabstand, damit es nicht dauernd wackelt */
export const useImpactTimes = (words: CaptionWord[], minGap = 1.4) =>
  useMemo(() => {
    const out: number[] = [];
    for (const w of words) {
      if (!isEmphasis(w.word)) continue;
      if (out.length && w.start - out[out.length - 1] < minGap) continue;
      out.push(w.start);
    }
    return out;
  }, [words, minGap]);

/** Kamera-Wackeln: kurz und kräftig bei jedem Impact, klingt schnell ab */
export const Shake: React.FC<{impacts: number[]; children: React.ReactNode}> = ({impacts, children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const last = impacts.filter((s) => s <= t).pop();
  let x = 0;
  let y = 0;
  let rot = 0;
  let zoom = 1;
  if (last !== undefined) {
    const age = (t - last) * fps; // Frames seit dem Impact
    if (age < 10) {
      const k = (1 - age / 10) ** 2;
      x = (random(`sx-${frame}`) - 0.5) * 46 * k;
      y = (random(`sy-${frame}`) - 0.5) * 46 * k;
      rot = (random(`sr-${frame}`) - 0.5) * 2.2 * k;
      zoom = 1 + 0.06 * k;
    }
  }
  return (
    <AbsoluteFill style={{transform: `translate(${x}px, ${y}px) rotate(${rot}deg) scale(${zoom})`}}>{children}</AbsoluteFill>
  );
};

/** Glitch-Übergang: farbige Streifen und Versatz in den ersten Frames einer Szene */
export const GlitchCut: React.FC<{seed: number; retro: boolean; sport?: boolean; space?: boolean}> = ({seed, retro, sport = false, space = false}) => {
  const frame = useCurrentFrame();
  if (frame > 6) return null;
  const strength = 1 - frame / 7;
  const colors = retro
    ? [theme.cyan, theme.magenta, theme.green]
    : sport
      ? [theme.pitch, theme.white, theme.white]
      : space
        ? [theme.hud, theme.white, theme.nasaOrange]
        : [theme.white, theme.red, theme.yellow];
  const bars = Array.from({length: 7}, (_, i) => {
    const r = (k: string) => random(`g-${seed}-${frame}-${i}-${k}`);
    return {
      top: r('t') * 1920,
      h: 8 + r('h') * 90,
      x: (r('x') - 0.5) * 260 * strength,
      c: colors[Math.floor(r('c') * colors.length)],
      o: 0.25 + r('o') * 0.5,
    };
  });
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {bars.map((b, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: b.x,
            top: b.top,
            width: 1080,
            height: b.h,
            background: b.c,
            opacity: b.o * strength,
            mixBlendMode: 'screen',
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

/** Dünner Fortschrittsbalken unten – Zuschauer sehen, dass es kurz ist, und bleiben dran */
export const ProgressBar: React.FC<{retro: boolean; sport?: boolean; space?: boolean}> = ({retro, sport = false, space = false}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = Math.min(1, frame / Math.max(1, durationInFrames - 1));
  return (
    <div style={{position: 'absolute', left: 0, bottom: 0, width: 1080, height: 12, background: 'rgba(255,255,255,0.18)'}}>
      <div
        style={{
          width: `${p * 100}%`,
          height: '100%',
          background: retro
            ? `linear-gradient(90deg, ${theme.cyan}, ${theme.magenta})`
            : sport
              ? theme.pitch
              : space
                ? `linear-gradient(90deg, ${theme.hud}, ${theme.nasaOrange})`
                : theme.yellow,
        }}
      />
    </div>
  );
};

/** Röhrenbildschirm-Look: Scanlines, leichte Wölbung, Farbsaum */
export const CRT: React.FC = () => {
  const frame = useCurrentFrame();
  const roll = (frame * 3) % 1920;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.28) 0px, rgba(0,0,0,0.28) 2px, transparent 2px, transparent 5px)',
          mixBlendMode: 'multiply',
        }}
      />
      {/* langsam durchlaufender heller Streifen wie bei alten Röhren */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: roll - 120,
          width: 1080,
          height: 120,
          background: 'linear-gradient(180deg, transparent, rgba(255,255,255,0.06), transparent)',
        }}
      />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,0.75) 100%)'}} />
      <AbsoluteFill style={{boxShadow: `inset 6px 0 0 rgba(255,43,214,0.12), inset -6px 0 0 rgba(0,240,255,0.12)`}} />
    </AbsoluteFill>
  );
};

/** Soundeffekte: Whoosh/Blip bei jedem Schnitt, dumpfer Schlag bei Impacts */
export const SoundEffects: React.FC<{scenes: Scene[]; impacts: number[]; retro: boolean; sport?: boolean; space?: boolean}> = ({
  scenes,
  impacts,
  retro,
  sport = false,
  space = false,
}) => {
  const {fps} = useVideoConfig();
  const cut = retro ? 'sfx/blip.wav' : sport ? 'sfx/kick.wav' : space ? 'sfx/radio.wav' : 'sfx/whoosh.wav';
  const hit = sport ? 'sfx/crowd.wav' : space ? 'sfx/rumble.wav' : 'sfx/hit.wav';
  return (
    <>
      {/* Stadion-Look: Anpfiff im allerersten Frame */}
      {sport ? (
        <Sequence from={0} durationInFrames={Math.round(fps * 0.8)} name="SFX Pfiff">
          <Audio src={staticFile('sfx/whistle.wav')} volume={0.5} />
        </Sequence>
      ) : null}
      {/* Weltraum-Look: NASA-Funkpiepton (Quindar) im allerersten Frame */}
      {space ? (
        <Sequence from={0} durationInFrames={Math.round(fps * 0.4)} name="SFX Quindar">
          <Audio src={staticFile('sfx/quindar.wav')} volume={0.35} />
        </Sequence>
      ) : null}
      {scenes.slice(1).map((s, i) => (
        <Sequence key={`cut-${i}`} from={Math.max(0, Math.round(s.start * fps) - 3)} durationInFrames={Math.round(fps * 0.8)} name="SFX Schnitt">
          <Audio src={staticFile(cut)} volume={0.35} />
        </Sequence>
      ))}
      {impacts.map((t, i) => (
        <Sequence key={`hit-${i}`} from={Math.round(t * fps)} durationInFrames={Math.round(fps * (sport ? 1.8 : space ? 1.4 : 0.6))} name="SFX Impact">
          <Audio src={staticFile(hit)} volume={sport ? 0.55 : space ? 0.6 : 0.45} />
        </Sequence>
      ))}
    </>
  );
};

/** Weltraum-Look: Display-Rahmen wie im Raumschiff / in der Missionskontrolle */
export const HUD: React.FC<{label?: string; delayed?: boolean}> = ({label, delayed = false}) => {
  const frame = useCurrentFrame();
  const blink = Math.floor(frame / 15) % 2 === 0;
  // "delayed": erst nach 1,5 s einblenden, damit der erste Frame nur Bild + Untertitel zeigt
  const appear = delayed ? Math.min(1, Math.max(0, (frame - 45) / 15)) : Math.min(1, frame / 12);
  const c = theme.hud;
  const corner = (pos: React.CSSProperties, rot: number) => (
    <div
      style={{
        position: 'absolute',
        width: 70,
        height: 70,
        borderTop: `5px solid ${c}`,
        borderLeft: `5px solid ${c}`,
        transform: `rotate(${rot}deg)`,
        opacity: 0.85 * appear,
        filter: `drop-shadow(0 0 8px ${c})`,
        ...pos,
      }}
    />
  );
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {corner({top: 110, left: 40}, 0)}
      {corner({top: 110, right: 40}, 90)}
      {corner({bottom: 230, right: 40}, 180)}
      {corner({bottom: 230, left: 40}, 270)}
      {label ? (
        <div
          style={{
            position: 'absolute',
            top: 130,
            left: 70,
            fontFamily: theme.spaceFont,
            fontWeight: 700,
            fontSize: 24,
            letterSpacing: 4,
            color: c,
            opacity: 0.9 * appear,
            textShadow: `0 0 10px ${c}`,
          }}
        >
          {label}
        </div>
      ) : null}
      <div
        style={{
          position: 'absolute',
          bottom: 250,
          left: 70,
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          fontFamily: theme.spaceFont,
          fontWeight: 700,
          fontSize: 22,
          letterSpacing: 4,
          color: c,
          opacity: 0.85 * appear,
        }}
      >
        <span style={{width: 14, height: 14, borderRadius: 7, background: theme.nasaOrange, opacity: blink ? 1 : 0.25}} />
        TELEMETRY
      </div>
      {/* sehr feine Scanlines für Bildschirm-Gefühl */}
      <AbsoluteFill
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, rgba(92,225,255,0.05) 0px, rgba(92,225,255,0.05) 1px, transparent 1px, transparent 4px)',
        }}
      />
    </AbsoluteFill>
  );
};
