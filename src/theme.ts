import {loadFont} from '@remotion/google-fonts/Anton';
import {loadFont as loadMono} from '@remotion/google-fonts/JetBrainsMono';
import {loadFont as loadPixel} from '@remotion/google-fonts/PressStart2P';
import {loadFont as loadLed} from '@remotion/google-fonts/DotGothic16';
import {loadFont as loadSpace} from '@remotion/google-fonts/Orbitron';

// Nur die benötigten Schnitte laden (latin-ext für Namen wie "Vulović")
const anton = loadFont('normal', {weights: ['400'], subsets: ['latin', 'latin-ext']});
const mono = loadMono('normal', {weights: ['400', '700'], subsets: ['latin', 'latin-ext']});
const pixel = loadPixel('normal', {weights: ['400'], subsets: ['latin', 'latin-ext']});
const led = loadLed('normal', {weights: ['400'], subsets: ['latin']});
const orbitron = loadSpace('normal', {weights: ['700', '900'], subsets: ['latin']});

// Zentrale Marken-Werte. Hier anpassen, dann gilt es für alle Shorts.
export const theme = {
  display: anton.fontFamily,
  mono: mono.fontFamily,
  pixel: pixel.fontFamily,
  /** LED-Anzeigetafel (Stadion-Look) */
  ledFont: led.fontFamily,
  /** Weltraum-Look (HUD, Missionsuhr) */
  spaceFont: orbitron.fontFamily,
  yellow: '#FFD400',
  red: '#E8322B',
  white: '#FFFFFF',
  black: '#0B0B0C',
  /** Retro-Look: Neonfarben */
  cyan: '#00F0FF',
  magenta: '#FF2BD6',
  green: '#39FF14',
  /** Stadion-Look */
  pitch: '#00D26A',
  ledColor: '#FFB000',
  /** Weltraum-Look */
  hud: '#5CE1FF',
  nasaOrange: '#FF6A1A',
  /** Untertitel sitzen im mittleren Bereich, damit sie nicht unter YouTubes UI verschwinden */
  captionY: 1180,
  /** Sicherer Bereich oben (Zähler, Dateline) */
  topSafe: 250,
};

/** Wörter, die "knallen": Zahlen und GROSSGESCHRIEBENES */
export const isEmphasis = (word: string) =>
  /\d/.test(word) || (word.length > 2 && word === word.toUpperCase() && /[A-Z]/.test(word));
