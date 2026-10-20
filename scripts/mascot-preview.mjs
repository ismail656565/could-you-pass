// Vorschau für das Maskottchen Q-Bit: Standbilder aller Kostüme + kurze Testvideos mit Ton.
// Aufruf: node scripts/mascot-preview.mjs   → Ergebnisse in preview/
import {spawnSync} from 'node:child_process';
import {mkdirSync, readFileSync, writeFileSync} from 'node:fs';

mkdirSync('preview', {recursive: true});
mkdirSync('out', {recursive: true});
const FPS = 30;
const run = (args) => {
  const r = spawnSync('npx', ['remotion', ...args], {stdio: 'inherit'});
  if (r.status !== 0) throw new Error('remotion ' + args.join(' ') + ' fehlgeschlagen');
};
const props = (name, story) => {
  const f = `out/.props-${name}.json`;
  writeFileSync(f, JSON.stringify(story));
  return `--props=${f}`;
};

const short = JSON.parse(readFileSync('stories/halloween-trap-3-1.json', 'utf8'));
const long = JSON.parse(readFileSync('stories/halloween-quiz-35.json', 'utf8'));
const q0 = short.questions[0];
const l1 = long.questions[1];

// Stimmungen im Short (Halloween)
const moments = {talk: q0.start + 1.2, tense: q0.reveal - 1.5, happy: q0.reveal + 0.35};
for (const [k, t] of Object.entries(moments)) run(['still', 'Quiz', `preview/short-${k}.png`, props('s', short), `--frame=${Math.round(t * FPS)}`]);

// alle Kostüme (Short, Moment "talk")
for (const c of ['standard', 'football', 'christmas', 'science', 'history']) {
  run(['still', 'Quiz', `preview/short-costume-${c}.png`, props(`c-${c}`, {...short, mascot: c}), `--frame=${Math.round(moments.talk * FPS)}`]);
}

// Langvideo: Frage 2 sprechen + Auflösung
run(['still', 'QuizLong', 'preview/long-talk.png', props('l', long), `--frame=${Math.round((l1.start + 1) * FPS)}`]);
run(['still', 'QuizLong', 'preview/long-happy.png', props('l', long), `--frame=${Math.round((l1.reveal + 0.35) * FPS)}`]);
run(['still', 'QuizLong', 'preview/long-football.png', props('lf', {...long, mascot: 'football', header: 'PREMIER LEAGUE QUIZ'}), `--frame=${Math.round((l1.start + 1) * FPS)}`]);

// Testvideos mit Ton (Lippen-Sync prüfen)
run(['render', 'Quiz', 'out/short.mp4', props('s', short), '--concurrency=100%']);
run(['render', 'QuizLong', 'out/long.mp4', props('l', long), `--frames=0-${Math.round(l1.end * FPS)}`, '--concurrency=100%']);
for (const [i, o, s] of [['out/short.mp4', 'preview/short-halloween.mp4', '540:960'], ['out/long.mp4', 'preview/long-halloween.mp4', '960:540']]) {
  const r = spawnSync('ffmpeg', ['-y', '-i', i, '-vf', `scale=${s}`, '-c:v', 'libx264', '-crf', '30', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '96k', o], {stdio: 'inherit'});
  if (r.status !== 0) throw new Error('ffmpeg fehlgeschlagen');
}
console.log('Vorschau fertig in preview/');
