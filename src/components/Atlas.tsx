// Gemeinsame Bausteine für den Atlas-/Druck-Look (Layout "atlas"): Papier, zwei Druckfarben, Serifen-Überschrift.
// Regeln des Looks: keine Emojis, kein Maskottchen, keine bunten Template-Kacheln.
import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {loadFont as loadSerif} from '@remotion/google-fonts/Fraunces';
import {loadFont as loadSans} from '@remotion/google-fonts/BarlowCondensed';

export const serif = loadSerif('normal', {weights: ['600', '900'], subsets: ['latin', 'latin-ext']}).fontFamily;
export const serifItalic = loadSerif('italic', {weights: ['900'], subsets: ['latin', 'latin-ext']}).fontFamily;
export const sans = loadSans('normal', {weights: ['500', '600', '700'], subsets: ['latin', 'latin-ext']}).fontFamily;

export const A = {
  paper: '#F1EADB',
  land: '#DDD2BA',
  coast: '#BFB196',
  grid: '#DDD3BE',
  ink: '#1E1A15',
  soft: '#7B7163',
  red: '#E2532F',
  blue: '#1F4E79',
};

/** Emojis und Pfeil-Symbole entfernen (Texte aus der Queue enthalten oft welche) */
export const stripEmoji = (s?: string) =>
  (s ?? '')
    .replace(/[\p{Extended_Pictographic}\u{1F1E6}-\u{1F1FF}\u{FE0F}\u{200D}\u{20E3}]/gu, '')
    .replace(/\s{2,}/g, ' ')
    .trim();

export const Kicker: React.FC<{brand?: string; section: string; right?: string}> = ({brand, section, right}) => (
  <div style={{position: 'absolute', left: 64, right: 64, top: 176, display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontFamily: sans, fontWeight: 600, fontSize: 34, letterSpacing: 5, color: A.soft, whiteSpace: 'nowrap'}}>
    <span>
      {(brand ?? 'COULD YOU PASS?').toUpperCase()} <span style={{color: A.coast}}>/</span> {stripEmoji(section).toUpperCase()}
    </span>
    <span style={{color: A.ink}}>{right}</span>
  </div>
);

/** Druckkörnung + leichte Randabdunklung – liegt über allem */
export const Grain: React.FC = () => (
  <>
    <AbsoluteFill style={{mixBlendMode: 'multiply', opacity: 0.9, pointerEvents: 'none'}}>
      <Img src={staticFile('bilder/paper-grain.jpg')} style={{width: 1080, height: 1920}} />
    </AbsoluteFill>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(60,45,20,0.16) 100%)', pointerEvents: 'none'}} />
  </>
);
