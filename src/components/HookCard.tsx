import React from 'react';
import {AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme} from '../theme';

/**
 * Riesiger Hook-Text, der schon im allerersten Frame voll sichtbar ist.
 * Wer beim Wischen kurz stoppt, liest ihn, bevor überhaupt ein Wort gesprochen ist.
 * Bleibt ca. 1,8 s stehen, dann fliegt er raus.
 */
export const HOOK_SECONDS = 1.8;

export const HookCard: React.FC<{text: string; retro: boolean; sport?: boolean; space?: boolean}> = ({text, retro, sport = false, space = false}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const end = HOOK_SECONDS * fps;

  // Frame 0 ist schon voll sichtbar (kein Einblenden!), nur ein leichter "Schlag"
  const slam = interpolate(frame, [0, 5], [1.12, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.back(3))});
  const out = interpolate(frame, [end - 6, end], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});
  const jitter = frame < 8 ? (random(`hj-${frame}`) - 0.5) * 14 * (1 - frame / 8) : 0;

  const words = text.split(/\s+/);
  // Schrift so groß wie möglich, aber das längste Wort muss in eine Zeile passen
  const longest = Math.max(...words.map((w) => w.length));
  const size = retro
    ? Math.min(92, Math.floor(900 / longest))
    : space
      ? Math.min(120, Math.floor(900 / (longest * 0.82)))
      : Math.min(168, Math.floor(900 / (longest * 0.52)));
  const accent = retro ? theme.magenta : sport ? theme.pitch : space ? theme.nasaOrange : theme.red;

  return (
    <AbsoluteFill style={{alignItems: 'center', pointerEvents: 'none'}}>
      <div
        style={{
          position: 'absolute',
          top: 300,
          width: 980,
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: retro ? '8px 26px' : '0 26px',
          transform: `translate(${jitter + out * 1200}px, 0) scale(${slam}) rotate(${-3 + out * 8}deg)`,
          opacity: 1 - out * 0.3,
        }}
      >
        {words.map((w, i) => (
          <span
            key={i}
            style={{
              fontFamily: retro ? theme.pixel : space ? theme.spaceFont : theme.display,
              fontWeight: space ? 900 : undefined,
              fontSize: size,
              lineHeight: retro ? 1.25 : 0.98,
              textTransform: 'uppercase',
              color: i % 2 === 1 ? (space ? theme.hud : theme.yellow) : theme.white,
              background: i === 0 ? accent : 'transparent',
              padding: i === 0 ? '0 14px' : 0,
              WebkitTextStroke: i === 0 ? '0' : retro ? '7px black' : '10px black',
              paintOrder: 'stroke fill',
              textShadow: retro ? '6px 6px 0 #000' : space ? `0 0 30px ${theme.hud}AA, 0 10px 30px rgba(0,0,0,0.7)` : '0 10px 30px rgba(0,0,0,0.7)',
              display: 'inline-block',
            }}
          >
            {w}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};
