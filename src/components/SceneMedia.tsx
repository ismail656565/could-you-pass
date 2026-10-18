import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  OffthreadVideo,
  interpolate,
  random,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {Scene} from '../types';
import {theme} from '../theme';
import {GlitchCut} from './Energy';

// Ein Hintergrund-Abschnitt: Video, Bild (Ken-Burns) oder Archivmaterial.
// Läuft innerhalb einer <Sequence>, frame beginnt also bei 0.
export const SceneMedia: React.FC<{
  scene: Scene;
  index: number;
  energy?: 'normal' | 'high' | 'clean';
  retro?: boolean;
  sport?: boolean;
  space?: boolean;
  flashes?: boolean;
}> = ({scene, index, energy = 'normal', retro = false, sport = false, space = false, flashes = true}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = Math.max(1, (scene.end - scene.start) * fps);
  const high = energy === 'high';
  const clean = energy === 'clean';

  // Blitz am Szenenanfang – typischer Shorts-Schnitt, hält die Aufmerksamkeit
  const flash = interpolate(frame, [0, high ? 3 : 4], [index === 0 || !flashes || clean ? 0 : high ? 0.6 : 0.35, 0], {
    extrapolateRight: 'clamp',
  });

  // Zoom-Punch: Bild "springt" beim Schnitt kurz heran und federt zurück
  // (auch in Szene 1: das allererste Bild ist schon in Bewegung)
  const punch = high
    ? interpolate(frame, [0, index === 0 ? 12 : 8], [index === 0 ? 1.35 : 1.22, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)})
    : 1;

  // Ken-Burns für Standbilder, leichter Zoom auch bei Videos (bei "high" schneller)
  const zoomIn = scene.zoom !== 'out';
  const kb = high ? 0.3 : clean ? 0.1 : 0.17;
  const scale =
    punch *
    (scene.kind === 'video'
      ? interpolate(frame, [0, len], [1.0, high ? 1.12 : 1.06])
      : interpolate(frame, [0, len], zoomIn ? [1.05, 1.05 + kb] : [1.05 + kb, 1.05]));
  const drift = interpolate(frame, [0, len], [0, (index % 2 === 0 ? -30 : 30) * (high ? 2 : 1)]);

  const isArchive = scene.kind === 'archive';
  const filter = isArchive
    ? 'grayscale(0.85) sepia(0.35) contrast(1.15) brightness(0.9)'
    : retro
      ? 'contrast(1.2) saturate(1.45)'
      : sport
        ? 'contrast(1.15) saturate(1.35) brightness(1.03)'
        : space
          ? 'contrast(1.18) saturate(1.15) brightness(0.95) hue-rotate(-6deg)'
          : 'contrast(1.05) saturate(1.1)';

  const mediaStyle: React.CSSProperties = {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    transform: `scale(${scale}) translateX(${drift}px)`,
    filter,
  };

  const isVideoFile = scene.src ? /\.(mp4|mov|webm|m4v)$/i.test(scene.src) : false;

  let media: React.ReactNode;
  if (!scene.src) {
    media = <Placeholder scene={scene} index={index} />;
  } else if (isVideoFile) {
    media = (
      <OffthreadVideo
        src={staticFile(scene.src)}
        muted
        startFrom={Math.round((scene.trimStart ?? 0) * fps)}
        style={mediaStyle}
      />
    );
  } else {
    media = <Img src={staticFile(scene.src)} style={mediaStyle} />;
  }

  return (
    <AbsoluteFill style={{backgroundColor: theme.black, overflow: 'hidden'}}>
      {media}
      {/* Abdunkeln oben und unten, damit Text immer lesbar ist */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 28%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.65) 100%)',
        }}
      />
      {isArchive ? <ArchiveTreatment label={scene.label} /> : null}
      {!isArchive && space && scene.label ? <SpaceTag label={scene.label} /> : null}
      <AbsoluteFill style={{backgroundColor: retro ? theme.cyan : space ? '#DDF6FF' : 'white', opacity: flash}} />
      {high && flashes && index > 0 ? <GlitchCut seed={index} retro={retro} sport={sport} space={space} /> : null}
    </AbsoluteFill>
  );
};

const ArchiveTreatment: React.FC<{label?: string}> = ({label}) => {
  const frame = useCurrentFrame();
  // Filmkorn: zufällige Verschiebung pro Frame
  const gx = Math.floor(random(`gx-${frame}`) * 200);
  const gy = Math.floor(random(`gy-${frame}`) * 200);
  const flicker = 0.9 + random(`fl-${frame}`) * 0.1;
  return (
    <>
      <AbsoluteFill
        style={{
          opacity: 0.22,
          mixBlendMode: 'overlay',
          backgroundImage:
            'repeating-radial-gradient(circle at 17% 32%, rgba(255,255,255,0.9) 0 1px, transparent 1px 3px)',
          backgroundSize: '7px 7px',
          backgroundPosition: `${gx}px ${gy}px`,
        }}
      />
      <AbsoluteFill style={{backgroundColor: 'black', opacity: 1 - flicker}} />
      {/* Vignette */}
      <AbsoluteFill
        style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.7) 100%)'}}
      />
      {label ? (
        <div
          style={{
            position: 'absolute',
            right: 56,
            top: 470,
            fontFamily: theme.mono,
            fontSize: 30,
            letterSpacing: 4,
            color: theme.white,
            opacity: 0.85,
            padding: '8px 16px',
            border: '2px solid rgba(255,255,255,0.7)',
          }}
        >
          {label}
        </div>
      ) : null}
    </>
  );
};

/** Weltraum-Look: Namensschild wie eine Bildschirm-Markierung, tippt sich Buchstabe für Buchstabe ein */
const SpaceTag: React.FC<{label: string}> = ({label}) => {
  const frame = useCurrentFrame();
  const shown = label.slice(0, Math.max(0, Math.floor((frame - 4) * 1.6)));
  if (!shown) return null;
  const c = theme.hud;
  return (
    <div
      style={{
        position: 'absolute',
        right: 56,
        top: 470,
        display: 'flex',
        alignItems: 'center',
        gap: 14,
        fontFamily: theme.spaceFont,
        fontWeight: 700,
        fontSize: 32,
        letterSpacing: 4,
        color: c,
        padding: '10px 18px',
        border: `3px solid ${c}`,
        background: 'rgba(0,12,24,0.6)',
        boxShadow: `0 0 18px ${c}55`,
        textShadow: `0 0 10px ${c}`,
      }}
    >
      <span style={{width: 12, height: 12, background: theme.nasaOrange}} />
      {shown}
    </div>
  );
};

// Wird gezeigt, solange einer Szene noch keine Datei zugewiesen ist
const Placeholder: React.FC<{scene: Scene; index: number}> = ({scene, index}) => {
  const hues = [212, 18, 260, 160, 340, 45];
  const h = hues[index % hues.length];
  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(160deg, hsl(${h} 45% 22%) 0%, hsl(${h} 35% 8%) 100%)`,
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          fontFamily: theme.mono,
          fontSize: 34,
          color: 'rgba(255,255,255,0.45)',
          textAlign: 'center',
          lineHeight: 1.5,
          marginTop: -420,
        }}
      >
        SZENE {index + 1} · {scene.kind.toUpperCase()}
        <br />
        {scene.start.toFixed(1)}s – {scene.end.toFixed(1)}s
      </div>
    </AbsoluteFill>
  );
};
