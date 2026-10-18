import React from 'react';
import {Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {CounterOverlay, Dateline} from '../types';
import {theme} from '../theme';

// Zähler, der von einem Wert auf einen anderen läuft (z. B. Höhe 33,330 FT -> 0 FT).
// Läuft innerhalb einer <Sequence>, frame beginnt bei 0.
export const Counter: React.FC<{c: CounterOverlay; retro?: boolean; sport?: boolean; space?: boolean}> = ({
  c,
  retro = false,
  sport = false,
  space = false,
}) => {
  if (sport) return <Scoreboard c={c} />;
  if (space) return <MissionClock c={c} />;
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = (c.end - c.start) * fps;

  const enter = spring({frame, fps, config: {damping: 16}});
  const exit = interpolate(frame, [len - 8, len], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const value = interpolate(frame, [6, len - 10], [c.from, c.to], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });
  const falling = c.to < c.from;
  const progress = Math.abs(value - c.from) / Math.max(1, Math.abs(c.to - c.from));

  return (
    <div
      style={{
        position: 'absolute',
        top: theme.topSafe,
        left: 0,
        right: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        opacity: exit,
        transform: `translateY(${interpolate(enter, [0, 1], [-40, 0])}px)`,
      }}
    >
      {c.label ? (
        <div style={{fontFamily: retro ? theme.pixel : theme.mono, fontSize: retro ? 26 : 32, letterSpacing: retro ? 3 : 8, color: retro ? theme.cyan : theme.white, opacity: 0.9}}>
          {c.label}
        </div>
      ) : null}
      <div
        style={{
          fontFamily: retro ? theme.pixel : theme.display,
          fontSize: retro ? 92 : 150,
          lineHeight: retro ? 1.4 : 1,
          color: falling && progress > 0.75 ? (retro ? theme.magenta : theme.red) : retro ? theme.yellow : theme.white,
          WebkitTextStroke: '6px black',
          paintOrder: 'stroke fill',
          fontVariantNumeric: 'tabular-nums',
        }}
      >
        {Math.round(value).toLocaleString('en-US')}
        {c.unit ? <span style={{fontSize: retro ? 40 : 70, marginLeft: 14}}>{c.unit}</span> : null}
      </div>
      {/* Fortschrittsbalken */}
      <div style={{width: 520, height: 10, background: 'rgba(255,255,255,0.25)', marginTop: 18, borderRadius: 5}}>
        <div
          style={{
            width: `${progress * 100}%`,
            height: '100%',
            background: retro ? (falling ? theme.magenta : theme.cyan) : falling ? theme.red : theme.yellow,
            borderRadius: 5,
          }}
        />
      </div>
    </div>
  );
};

// Datum/Ort-Zeile im Schreibmaschinen-Stil, z. B. "26 JAN 1972 · CZECHOSLOVAKIA"
export const DatelineBar: React.FC<{d: Dateline; retro?: boolean; sport?: boolean; space?: boolean}> = ({
  d,
  retro = false,
  sport = false,
  space = false,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = (d.end - d.start) * fps;
  const chars = Math.floor(interpolate(frame, [0, 18], [0, d.text.length], {extrapolateRight: 'clamp'}));
  const exit = interpolate(frame, [len - 8, len], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const cursorOn = Math.floor(frame / 8) % 2 === 0 && chars < d.text.length + 1;

  return (
    <div
      style={{
        position: 'absolute',
        top: theme.topSafe + 10,
        left: 56,
        opacity: exit,
        display: 'flex',
        alignItems: 'center',
        gap: 16,
      }}
    >
      <div style={{width: 14, height: 14, borderRadius: retro ? 0 : 7, background: retro ? theme.magenta : sport ? theme.pitch : space ? theme.nasaOrange : theme.red}} />
      <div
        style={{
          fontFamily: retro ? theme.pixel : space ? theme.spaceFont : theme.mono,
          fontSize: retro ? 26 : space ? 32 : 40,
          fontWeight: retro ? 400 : 700,
          letterSpacing: 3,
          color: retro ? theme.green : sport ? theme.black : space ? theme.hud : theme.white,
          background: sport ? theme.white : space ? 'rgba(2,12,24,0.75)' : 'rgba(0,0,0,0.7)',
          border: space ? `2px solid ${theme.hud}` : 'none',
          padding: '10px 18px',
        }}
      >
        {d.text.slice(0, chars)}
        <span style={{opacity: cursorOn ? 1 : 0}}>▌</span>
      </div>
    </div>
  );
};

/**
 * Stadion-Look: LED-Anzeigetafel. Der Zähler läuft hoch wie ein echter Spielstand,
 * die Ziffern "klicken" bei jeder Änderung kurz auf.
 * Label wird als Mannschaften gelesen, wenn es "A – B" oder "A - B" enthält.
 */
const Scoreboard: React.FC<{c: CounterOverlay}> = ({c}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = (c.end - c.start) * fps;
  const enter = spring({frame, fps, config: {damping: 14}});
  const exit = interpolate(frame, [len - 8, len], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const value = Math.round(
    interpolate(frame, [6, len - 10], [c.from, c.to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.quad)}),
  );
  const prev = Math.round(
    interpolate(frame - 1, [6, len - 10], [c.from, c.to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.quad)}),
  );
  const tick = value !== prev ? 1.06 : 1;
  const teams = c.label && /\s[–-]\s/.test(c.label) ? c.label.split(/\s[–-]\s/) : null;
  const digits: React.CSSProperties = {
    fontFamily: theme.ledFont,
    fontSize: 150,
    lineHeight: 1,
    color: theme.ledColor,
    textShadow: `0 0 18px ${theme.ledColor}, 0 0 42px ${theme.ledColor}88`,
    fontVariantNumeric: 'tabular-nums',
  };
  return (
    <div
      style={{
        position: 'absolute',
        top: theme.topSafe,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        opacity: exit,
        transform: `translateY(${interpolate(enter, [0, 1], [-60, 0])}px)`,
      }}
    >
      <div
        style={{
          background: 'linear-gradient(180deg, #161616, #050505)',
          border: '6px solid #2a2a2a',
          borderRadius: 18,
          padding: '18px 34px 22px',
          boxShadow: '0 20px 50px rgba(0,0,0,0.7)',
          minWidth: 620,
          backgroundImage:
            'radial-gradient(rgba(255,176,0,0.07) 1px, transparent 1.5px), linear-gradient(180deg, #161616, #050505)',
          backgroundSize: '8px 8px, 100% 100%',
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: teams ? 'space-between' : 'center',
            fontFamily: theme.display,
            fontSize: 40,
            letterSpacing: 4,
            color: theme.white,
            marginBottom: 6,
          }}
        >
          {teams ? (
            <>
              <span>{teams[0]}</span>
              <span>{teams[1]}</span>
            </>
          ) : (
            <span>{c.label}</span>
          )}
        </div>
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 24}}>
          <span style={{...digits, transform: `scale(${tick})`, display: 'inline-block'}}>{value.toLocaleString('en-US')}</span>
          {c.unit ? <span style={{...digits, fontSize: 110}}>{c.unit}</span> : null}
        </div>
      </div>
    </div>
  );
};

/**
 * Weltraum-Look: Missionsuhr. Mit Einheit "MET" läuft sie als "T+ 00:00:36" hoch,
 * sonst als HUD-Zahl mit Einheit.
 */
const MissionClock: React.FC<{c: CounterOverlay}> = ({c}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = (c.end - c.start) * fps;
  const enter = spring({frame, fps, config: {damping: 15}});
  const exit = interpolate(frame, [len - 8, len], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const value = interpolate(frame, [6, len - 10], [c.from, c.to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const met = c.unit === 'MET';
  const pad = (n: number) => String(Math.floor(n)).padStart(2, '0');
  const text = met
    ? `T+ ${pad(value / 3600)}:${pad((value % 3600) / 60)}:${pad(value % 60)}`
    : Math.round(value).toLocaleString('en-US');
  return (
    <div
      style={{
        position: 'absolute',
        top: theme.topSafe + 20,
        left: 0,
        right: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        opacity: exit,
        transform: `scale(${interpolate(enter, [0, 1], [0.85, 1])})`,
      }}
    >
      {c.label ? (
        <div style={{fontFamily: theme.spaceFont, fontWeight: 700, fontSize: 26, letterSpacing: 8, color: theme.hud, marginBottom: 10}}>
          {c.label}
        </div>
      ) : null}
      <div
        style={{
          fontFamily: theme.spaceFont,
          fontWeight: 900,
          fontSize: met ? 96 : 130,
          color: theme.white,
          padding: '14px 30px',
          border: `3px solid ${theme.hud}`,
          background: 'rgba(2,12,24,0.7)',
          textShadow: `0 0 22px ${theme.hud}`,
          boxShadow: `0 0 30px ${theme.hud}55, inset 0 0 30px ${theme.hud}22`,
          fontVariantNumeric: 'tabular-nums',
        }}
      >
        {text}
        {!met && c.unit ? <span style={{fontSize: 60, marginLeft: 16, color: theme.hud}}>{c.unit}</span> : null}
      </div>
    </div>
  );
};
