import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Story} from './types';
import {SceneMedia} from './components/SceneMedia';
import {Captions, estimateWords} from './components/Captions';
import {Counter, DatelineBar} from './components/Overlays';
import {EndStamp} from './components/EndStamp';
import {CRT, HUD, ProgressBar, Shake, SoundEffects, useImpactTimes} from './components/Energy';
import {HOOK_SECONDS, HookCard} from './components/HookCard';
import {theme} from './theme';

/**
 * Länge des End-Stempels in Sekunden.
 * Standard 0 = kein Stempel: Das Video endet direkt mit dem letzten Wort, damit
 * es nahtlos in den Anfang übergeht (Loop). Der Stempel kostete Zuschauer am Ende.
 * Muss zu END_STAMP_SECONDS in scripts/whisper_words.py passen.
 */
export const END_STAMP_SECONDS = 0;

export const WildlyTrue: React.FC<Story> = (story) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const storyEnd = story.durationInSeconds - END_STAMP_SECONDS;
  const retro = story.style === 'retro';
  const sport = story.style === 'sport';
  const space = story.style === 'space';
  const high = story.energy === 'high';
  // "clean": ruhiger Start ohne Effekte – Test gegen das Wegwischen in der ersten Sekunde
  const clean = story.energy === 'clean';
  const energy = high ? 'high' : clean ? 'clean' : 'normal';

  // Echte Whisper-Wörter, sonst geschätzte Zeiten aus dem Skript (für Vorschauen)
  const words = useMemo(
    () => (story.captions && story.captions.length > 0 ? story.captions : estimateWords(story.script, 0.1, storyEnd - 0.2)),
    [story.captions, story.script, storyEnd],
  );
  const impacts = useImpactTimes(high ? words : []);

  const picture = (
    <>
      {story.scenes.map((scene, i) => (
        <Sequence
          key={`scene-${i}`}
          from={f(scene.start)}
          durationInFrames={Math.max(1, f(scene.end) - f(scene.start))}
          name={`Szene ${i + 1} (${scene.kind})`}
        >
          <SceneMedia scene={scene} index={i} energy={energy} retro={retro} sport={sport} space={space} flashes={story.flashes !== false} />
        </Sequence>
      ))}
      {retro ? <CRT /> : null}
      {space ? <HUD label={story.hudLabel} delayed={clean} /> : null}
    </>
  );

  return (
    <AbsoluteFill style={{backgroundColor: theme.black, overflow: 'hidden'}}>
      {/* Bild wackelt bei Impacts, Text bleibt ruhig und lesbar */}
      {high ? <Shake impacts={impacts}>{picture}</Shake> : picture}

      {(story.datelines ?? []).map((d, i) => (
        <Sequence key={`date-${i}`} from={f(d.start)} durationInFrames={Math.max(1, f(d.end) - f(d.start))} name="Dateline">
          <DatelineBar d={d} retro={retro} sport={sport} space={space} />
        </Sequence>
      ))}

      {(story.counters ?? []).map((c, i) => (
        <Sequence key={`counter-${i}`} from={f(c.start)} durationInFrames={Math.max(1, f(c.end) - f(c.start))} name="Zähler">
          <Counter c={c} retro={retro} sport={sport} space={space} />
        </Sequence>
      ))}

      {/* Untertitel starten erst nach dem Hook-Text, damit oben nichts doppelt steht */}
      <Sequence durationInFrames={Math.max(1, f(storyEnd))} name="Untertitel">
        <Captions words={story.hookText && !clean ? words.filter((w) => w.end > HOOK_SECONDS - 0.2) : words} energy={energy} retro={retro} sport={sport} space={space} />
      </Sequence>

      {story.hookText && !clean ? (
        <Sequence durationInFrames={f(HOOK_SECONDS)} name="Hook-Text">
          <HookCard text={story.hookText} retro={retro} sport={sport} space={space} />
        </Sequence>
      ) : null}

      {/* Marke dauerhaft klein in der Ecke statt Stempel am Ende */}
      <Watermark retro={retro} sport={sport} space={space} brand={story.brand} />
      {high ? <ProgressBar retro={retro} sport={sport} space={space} /> : null}

      {END_STAMP_SECONDS > 0 ? (
        <Sequence from={f(storyEnd)} name="End-Stempel">
          <EndStamp />
        </Sequence>
      ) : null}

      {story.audio ? <Audio src={staticFile(story.audio)} startFrom={f(story.audioStartFrom ?? 0)} /> : null}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.12} loop /> : null}
      {high ? <SoundEffects scenes={story.scenes} impacts={impacts} retro={retro} sport={sport} space={space} /> : null}
    </AbsoluteFill>
  );
};

const Watermark: React.FC<{retro: boolean; sport?: boolean; space?: boolean; brand?: string}> = ({retro, sport = false, space = false, brand}) => {
  const frame = useCurrentFrame();
  // erst nach dem Hook einblenden, damit die ersten Sekunden frei bleiben
  const opacity = interpolate(frame, [45, 60], [0, 0.8], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const color = retro ? theme.magenta : sport ? theme.pitch : space ? theme.hud : theme.red;
  return (
    <div
      style={{
        position: 'absolute',
        right: 48,
        top: 150,
        opacity,
        transform: 'rotate(-6deg)',
        border: `4px solid ${color}`,
        borderRadius: retro ? 0 : 6,
        padding: retro ? '10px 12px 6px' : '4px 12px 0',
        color,
        fontFamily: retro ? theme.pixel : space ? theme.spaceFont : theme.display,
        fontWeight: space ? 900 : undefined,
        fontSize: retro ? 22 : space ? 28 : 38,
        letterSpacing: 2,
        lineHeight: 1.05,
      }}
    >
      {brand ?? 'WILDLY TRUE'}
    </div>
  );
};
