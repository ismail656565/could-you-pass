import React from 'react';
import {Composition} from 'remotion';
import {WildlyTrue} from './WildlyTrue';
import type {Story} from './types';
import beispiel from '../stories/beispiel.json';
import {Quiz, type QuizStory} from './Quiz';
import {QuizLong, QuizThumb} from './QuizLong';
import quizDemo from '../stories/quiz-demo.json';
import {TrueSize, TrueSizeThumb, type TrueSizeStory} from './TrueSize';
import mapLie from '../stories/map-lie-1.json';

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
    </>
  );
};
