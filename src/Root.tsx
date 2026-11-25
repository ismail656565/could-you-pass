import React from 'react';
import {Composition} from 'remotion';
import {WildlyTrue} from './WildlyTrue';
import {WildlyTrueMotion, type MotionStory} from './WildlyTrueMotion';
import wtMotionDemo from '../stories/wt-motion-demo.json';
import type {Story} from './types';
import beispiel from '../stories/beispiel.json';
import {Quiz, type QuizStory} from './Quiz';
import {QuizLong, QuizThumb} from './QuizLong';
import quizDemo from '../stories/quiz-demo.json';
import {TrueSize, TrueSizeThumb, type TrueSizeStory} from './TrueSize';
import mapLie from '../stories/map-lie-1.json';
import {FlagDuel, type FlagDuelStory} from './FlagDuel';
import flagDuel from '../stories/flag-duel-1.json';
import {FlagBlitz, FlagBlitzThumb, type FlagBlitzStory} from './FlagBlitz';
import flagBlitzDemo from '../stories/flag-blitz-demo.json';

export const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
    <Composition
      id="WildlyTrue"
      component={WildlyTrue}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={Math.ceil((beispiel as Story).durationInSeconds * FPS)}
      defaultProps={beispiel as Story}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.ceil(props.durationInSeconds * FPS),
      })}
    />
    <Composition
      id="WildlyTrueMotion"
      component={WildlyTrueMotion}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={Math.ceil((wtMotionDemo as unknown as MotionStory).durationInSeconds * FPS)}
      defaultProps={wtMotionDemo as unknown as MotionStory}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.ceil(props.durationInSeconds * FPS),
      })}
    />
    <Composition
      id="Quiz"
      component={Quiz}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={Math.ceil((quizDemo as QuizStory).durationInSeconds * FPS)}
      defaultProps={quizDemo as QuizStory}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.ceil(props.durationInSeconds * FPS),
      })}
    />
    <Composition
      id="QuizLong"
      component={QuizLong}
      width={1920}
      height={1080}
      fps={FPS}
      durationInFrames={Math.ceil((quizDemo as QuizStory).durationInSeconds! * FPS)}
      defaultProps={quizDemo as QuizStory}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.ceil(props.durationInSeconds! * FPS),
      })}
    />
    <Composition id="QuizThumb" component={QuizThumb} width={1280} height={720} fps={FPS} durationInFrames={1} defaultProps={quizDemo as QuizStory} />
    <Composition
      id="TrueSize"
      component={TrueSize}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={Math.ceil((mapLie as unknown as TrueSizeStory).durationInSeconds * FPS)}
      defaultProps={mapLie as unknown as TrueSizeStory}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.ceil(props.durationInSeconds * FPS),
      })}
    />
    <Composition
      id="TrueSizeLong"
      component={TrueSize}
      width={1920}
      height={1080}
      fps={FPS}
      durationInFrames={Math.ceil((mapLie as unknown as TrueSizeStory).durationInSeconds * FPS)}
      defaultProps={mapLie as unknown as TrueSizeStory}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.ceil(props.durationInSeconds * FPS),
      })}
    />
    <Composition id="TrueSizeThumb" component={TrueSizeThumb} width={1280} height={720} fps={FPS} durationInFrames={1} defaultProps={mapLie as unknown as TrueSizeStory} />
    <Composition
      id="FlagDuel"
      component={FlagDuel}
      width={1080}
      height={1920}
      fps={FPS}
      durationInFrames={Math.ceil((flagDuel as unknown as FlagDuelStory).durationInSeconds * FPS)}
      defaultProps={flagDuel as unknown as FlagDuelStory}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.ceil(props.durationInSeconds * FPS),
      })}
    />
    <Composition
      id="FlagBlitz"
      component={FlagBlitz}
      width={1920}
      height={1080}
      fps={FPS}
      durationInFrames={Math.ceil((flagBlitzDemo as unknown as FlagBlitzStory).durationInSeconds * FPS)}
      defaultProps={flagBlitzDemo as unknown as FlagBlitzStory}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.ceil(props.durationInSeconds * FPS),
      })}
    />
    <Composition id="FlagBlitzThumb" component={FlagBlitzThumb} width={1280} height={720} fps={FPS} durationInFrames={1} defaultProps={flagBlitzDemo as unknown as FlagBlitzStory} />
    </>
  );
};
