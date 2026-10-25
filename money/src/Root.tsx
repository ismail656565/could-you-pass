import React from 'react';
import {Composition} from 'remotion';
import {MoneyShort} from './MoneyShort';
import {TOTAL, FPS} from './timeline';

export const RemotionRoot: React.FC = () => (
  <Composition id="MoneyShort" component={MoneyShort} durationInFrames={TOTAL} fps={FPS} width={1080} height={1920} />
);
