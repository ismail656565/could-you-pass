// Datenformat für ein einzelnes Short. Eine Story-Datei (stories/*.json) hat genau diese Form.

export type SceneKind = 'video' | 'image' | 'archive';

export type Scene = {
  /** Startzeit in Sekunden */
  start: number;
  /** Endzeit in Sekunden */
  end: number;
  /** video = Stock/KI-Clip, image = Standbild (Ken-Burns), archive = Archivmaterial (Körnung + Label) */
  kind: SceneKind;
  /** Dateiname in public/ (z. B. "clips/crash.mp4"). Leer = Platzhalter */
  src?: string;
  /** Archiv-Label, z. B. "ARCHIVE 1972" (nur bei kind=archive) */
  label?: string;
  /** Ken-Burns-Richtung bei Bildern */
  zoom?: 'in' | 'out';
  /** Sekunden, ab denen ein Video-Clip abgespielt wird */
  trimStart?: number;
};

export type CounterOverlay = {
  start: number;
  end: number;
  from: number;
  to: number;
  /** Einheit hinter der Zahl, z. B. "FT" */
  unit?: string;
  /** Kleine Zeile darüber, z. B. "ALTITUDE" */
  label?: string;
};

export type Dateline = {
  start: number;
  end: number;
  /** z. B. "26 JAN 1972 · CZECHOSLOVAKIA" */
  text: string;
};

export type CaptionWord = {
  word: string;
  start: number;
  end: number;
};

export type Story = {
  title: string;
  /** Gesamtlänge in Sekunden (inkl. End-Stempel) */
  durationInSeconds: number;
  /** Voiceover in public/, z. B. "audio/vesna.mp3". Leer = ohne Ton */
  audio?: string;
  /** Lautstärke einer optionalen Musik */
  music?: string;
  musicVolume?: number;
  /** Komplettes Skript. Wird für Untertitel benutzt, falls keine Whisper-Wörter vorliegen */
  script: string;
  /** Wort-Zeitstempel von Whisper (scripts/whisper_words.py) */
  captions?: CaptionWord[];
  scenes: Scene[];
  counters?: CounterOverlay[];
  datelines?: Dateline[];
  /** Quellen für den Faktencheck (erscheinen nicht im Video) */
  sources?: string[];
  /** Look: "classic" (Standard) oder "retro" (Pixel-Schrift, Neon, Röhrenbildschirm) */
  style?: 'classic' | 'retro' | 'sport' | 'space';
  /** Tempo: "normal" oder "high" (Zoom-Punches, Wackeln, Glitch, Soundeffekte, Fortschrittsbalken) */
  energy?: 'normal' | 'high' | 'clean';
  /** Riesiger Hook-Text, der ab dem ersten Frame steht (z. B. "BOMBED. STILL WORKS.") */
  hookText?: string;
  /** Sekunden, die am Anfang des Voiceovers übersprungen werden (Stille). Setzt whisper_words.py */
  audioStartFrom?: number;
  /** false = keine Blitze/Glitches an den Schnitten (z. B. bei Themen rund um Lichtempfindlichkeit) */
  flashes?: boolean;
  /** Kleine Beschriftung im HUD-Rahmen (Weltraum-Look), z. B. "APOLLO 12 // FLIGHT DATA" */
  hudLabel?: string;
  /** Kanalname im Wasserzeichen (Standard: WILDLY TRUE) */
  brand?: string;
  /** Sprache des Voiceovers für Whisper, z. B. "de" */
  language?: string;
};
