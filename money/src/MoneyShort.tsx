import React from 'react';
import {AbsoluteFill, Audio, interpolate, staticFile, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {Scene} from './Scene';
import {Overlay} from './Overlay';
import {TOTAL} from './timeline';

export const MoneyShort: React.FC = () => {
  const {width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: '#d6dde4'}}>
      <ThreeCanvas
        width={width}
        height={height}
        shadows
        gl={{antialias: true, preserveDrawingBuffer: true}}
        camera={{fov: 35, near: 0.01, far: 2000, position: [0, 1, -2]}}
      >
        <Scene />
      </ThreeCanvas>
      <Overlay />
      <Audio
        src={staticFile('music/cutscene-crush.mp3')}
        volume={(f) => interpolate(f, [0, 6, TOTAL - 40, TOTAL - 1], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}
      />
    </AbsoluteFill>
  );
};
