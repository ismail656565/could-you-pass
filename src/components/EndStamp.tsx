import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme} from '../theme';

// Wiedererkennbarer Abschluss: Stempel "WILDLY TRUE" knallt aufs Bild.
// Läuft innerhalb einer <Sequence>, frame beginnt bei 0.
export const EndStamp: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const hit = spring({frame, fps, config: {damping: 9, stiffness: 260, mass: 0.7}});
  const scale = interpolate(hit, [0, 1], [2.6, 1]);
  const opacity = interpolate(frame, [0, 3], [0, 1], {extrapolateRight: 'clamp'});
  const dim = interpolate(frame, [0, 6], [0, 0.55], {extrapolateRight: 'clamp'});
  // Kurzes Wackeln beim Aufprall
  const shake = frame < 10 ? Math.sin(frame * 2.4) * (10 - frame) * 1.2 : 0;
  const sub = interpolate(frame, [12, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <AbsoluteFill style={{backgroundColor: 'black', opacity: dim}} />
      <div
        style={{
          transform: `translate(${shake}px, ${-120 + shake * 0.5}px) rotate(-8deg) scale(${scale})`,
          opacity,
          border: `14px solid ${theme.red}`,
          borderRadius: 18,
          padding: '18px 44px 6px',
          color: theme.red,
          fontFamily: theme.display,
          fontSize: 170,
          lineHeight: 1,
          letterSpacing: 6,
          textAlign: 'center',
          background: 'rgba(255,255,255,0.06)',
        }}
      >
        WILDLY
        <br />
        TRUE
      </div>
      <div
        style={{
          position: 'absolute',
          top: 1260,
          opacity: sub,
          fontFamily: theme.mono,
          fontSize: 38,
          letterSpacing: 6,
          color: theme.white,
        }}
      >
        FOLLOW FOR MORE TRUE STORIES
      </div>
    </AbsoluteFill>
  );
};
