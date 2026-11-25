// Rendert eine Story-Datei zu einem fertigen Short.
// Aufruf:  npm run render -- stories/vesna.json
// Ergebnis: out/vesna.mp4
// Fehlende Clips/Bilder werden als Platzhalter gerendert (mit Hinweis).
import {spawnSync} from 'node:child_process';
import {existsSync, mkdirSync, readFileSync, rmSync, writeFileSync} from 'node:fs';
import {basename, extname, resolve} from 'node:path';

const file = process.argv[2];
if (!file) {
  console.error('Bitte eine Story-Datei angeben, z. B.: npm run render -- stories/vesna.json');
  process.exit(1);
}
const path = resolve(file);
if (!existsSync(path)) {
  console.error(`Datei nicht gefunden: ${path}`);
  process.exit(1);
}

const story = JSON.parse(readFileSync(path, 'utf8'));
const problems = [];
if (!story.durationInSeconds) problems.push('durationInSeconds fehlt');
const isQuiz = story.type === 'quiz';
const isAtlas = story.type === 'truesize';
const isFlag = story.type === 'flagduel';
const isBlitz = story.type === 'flagblitz';
if (isAtlas || isFlag || isBlitz) {
  if (!Array.isArray(story.rounds) || story.rounds.length === 0) problems.push('keine Runden');
} else if (isQuiz) {
  if (!Array.isArray(story.questions) || story.questions.length === 0) problems.push('keine Fragen');
} else if (!Array.isArray(story.scenes) || story.scenes.length === 0) problems.push('keine Szenen');
if (story.audio && !existsSync(resolve('public', story.audio))) problems.push(`Audio fehlt in public/: ${story.audio}`);
if (problems.length) {
  console.error('Bitte zuerst beheben:\n- ' + problems.join('\n- '));
  process.exit(1);
}

// Fehlende Dateien -> Platzhalter statt Abbruch
const missing = [];
for (const s of story.scenes ?? []) {
  if (s.src && !existsSync(resolve('public', s.src))) {
    missing.push(s.src);
    s.src = '';
  }
}
if (missing.length) {
  console.warn(`Hinweis: ${missing.length} Datei(en) fehlen noch, dort erscheint ein Platzhalter:`);
  for (const m of missing) console.warn(`  - public/${m}`);
}
if (!isQuiz && !isAtlas && !isFlag && !isBlitz && !story.captions?.length) console.warn('Hinweis: keine Whisper-Wörter – Untertitel-Timing wird nur geschätzt.');

mkdirSync('out', {recursive: true});
const name = basename(path, extname(path));
const out = `out/${name}.mp4`;
// Props als Datei ohne Leerzeichen im Pfad (Windows-sicher)
const propsFile = `out/.props-${name}.json`;
writeFileSync(propsFile, JSON.stringify(story));

const result = spawnSync('npx', [
  'remotion', 'render', isBlitz ? 'FlagBlitz' : isFlag ? 'FlagDuel' : isAtlas ? (story.format === 'long' ? 'TrueSizeLong' : 'TrueSize') : isQuiz ? (story.format === 'long' ? 'QuizLong' : 'Quiz') : story.look === 'motion' ? 'WildlyTrueMotion' : 'WildlyTrue', out, `--props=${propsFile}`,
  // Speicher sparen: weniger parallele Frames und kleiner Video-Cache (sonst "memory allocation failed")
  `--concurrency=${process.env.RENDER_CONCURRENCY || 2}`,
  '--offthreadvideo-cache-size-in-bytes=536870912',
  '--offthreadvideo-threads=2',
  // optional: eigener Browser (z. B. in Umgebungen, in denen der mitgelieferte keine Schriften laden darf)
  ...(process.env.BROWSER_EXECUTABLE ? [`--browser-executable=${process.env.BROWSER_EXECUTABLE}`] : []),
  // optional: zusätzliche CLI-Flags (z. B. lokal hinter einem Proxy: --ignore-certificate-errors)
  ...(process.env.REMOTION_EXTRA ? process.env.REMOTION_EXTRA.split(' ').filter(Boolean) : []),
], {
  stdio: 'inherit',
  shell: process.platform === 'win32',
});
rmSync(propsFile, {force: true});
if (result.status === 0) console.log(`\nFertig: ${out}`);
process.exit(result.status ?? 1);
