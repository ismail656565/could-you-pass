import { sealVisualTrack } from "@hypit/composition";
import type { VisualElement } from "@hypit/composition";
import { htmlVisual } from "@hypit/html-program";
import type { FontStackRef } from "@hypit/media";
import type { Timeline } from "@hypit/timeline";
import type { SpatialFrame } from "@hypit/spatial";
import { assertTemporalWindowFor } from "@hypit/temporal";
import type { TemporalInstant, TemporalWindow } from "@hypit/temporal";

export type QuizKind = "hook" | "question" | "option" | "answer" | "end";
export type Message = { id: string; kind: QuizKind; text: string; at: TemporalInstant };
export type QuizOptions = { id: string; title: string; entranceFrames: number };

type Group = { question: number; options: number[]; answer: number; start: number; reveal: number; correct: number; end: number };

const LETTERS = ["A", "B", "C", "D"];

/** COULD YOU PASS? quiz: hook, question cards, countdown, reveal and end card in one scene. */
export function renderQuiz(timeline: Timeline, within: SpatialFrame, window: TemporalWindow,
  font: FontStackRef, items: readonly Message[], options: QuizOptions) {
  assertTemporalWindowFor(window, { subjectId: options.id, timeline });
  if (!Number.isSafeInteger(options.entranceFrames) || options.entranceFrames < 1) throw new Error("Quiz entrance-frames must be a positive integer.");
  if (items.some(item => item.at.frame < window.span.startFrame || item.at.frame >= window.span.endFrameExclusive)) throw new Error("Quiz items must appear inside the scene's window.");
  const rel = (item: Message) => item.at.frame - window.span.startFrame;
  const total = window.span.endFrameExclusive - window.span.startFrame;

  // Group items: question → options → answer.
  const groups: Group[] = [];
  let hook = -1, endCard = -1;
  items.forEach((item, index) => {
    if (item.kind === "hook") hook = index;
    else if (item.kind === "end") endCard = index;
    else if (item.kind === "question") groups.push({ question: index, options: [], answer: -1, start: rel(item), reveal: 0, correct: 0, end: total });
    else {
      const group = groups.at(-1);
      if (!group) throw new Error("Options and answers must follow a question.");
      if (item.kind === "option") group.options.push(index);
      else { group.answer = index; group.reveal = rel(item); group.correct = LETTERS.indexOf(item.text.trim().toUpperCase()); }
    }
  });
  groups.forEach((group, i) => {
    if (group.answer < 0 || group.options.length < 2 || group.options.length > 4 || group.correct < 0 || group.correct >= group.options.length)
      throw new Error(`Question ${i + 1} needs 2–4 options and an answer letter that names one of them.`);
    group.end = groups[i + 1]?.start ?? (endCard >= 0 ? rel(items[endCard]!) : total);
  });

  let order = 0;
  const text = (id: string, value: string, size: number, color: string): VisualElement => ({
    id, kind: "text", parent: "quiz", order: ++order, text: value, fonts: font.faces,
    style: [{ name: "font-size", value: `${size}px` }, { name: "line-height", value: 1.12 }, { name: "color", value: color }],
  });
  const children: VisualElement[] = [
    text("brand", "COULD YOU PASS?", 58, "#FFD400"),
    text("topic", options.title.toUpperCase(), 30, "#ffffff"),
    text("n3", "3", 120, "#ffffff"), text("n2", "2", 120, "#ffffff"), text("n1", "1", 120, "#ffffff"),
    text("plus", "+1", 84, "#39FF14"),
  ];
  if (hook >= 0) {
    const [first, ...rest] = items[hook]!.text.split("|");
    children.push(text("hook-a", first!.trim(), 70, "#ffffff"), text("hook-b", rest.join(" ").trim(), 132, "#FFD400"));
  }
  if (endCard >= 0) {
    const [first, ...rest] = items[endCard]!.text.split("|");
    children.push(text("end-a", first!.trim(), 96, "#FFD400"), text("end-b", rest.join(" ").trim(), 54, "#ffffff"));
  }
  groups.forEach((group, g) => {
    children.push(text(`count-${g}`, `QUESTION ${g + 1}/${groups.length}`, 34, "#c9b8ff"), text(`q-${g}`, items[group.question]!.text, 72, "#ffffff"));
    group.options.forEach((option, o) => children.push(text(`l-${g}-${o}`, LETTERS[o]!, 54, "#1b1240"), text(`o-${g}-${o}`, items[option]!.text, 56, "#ffffff")));
  });

  const qbit = `<svg class="qbit" viewBox="0 0 300 380"><ellipse cx="150" cy="352" rx="90" ry="12" fill="#000" opacity=".3"/>
    <g class="qb-body"><g class="qb-ant"><path d="M150 112 Q146 96 150 82" stroke="#2b2250" stroke-width="6" fill="none" stroke-linecap="round"/>
    <circle cx="150" cy="62" r="23" fill="#7cf2d4" stroke="#2b2250" stroke-width="5"/>
    <path d="M141 56 Q141 46 150 46 Q160 46 160 55 Q160 61 150 64 L150 69" stroke="#2b2250" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="150" cy="77" r="3.5" fill="#2b2250"/></g>
    <ellipse cx="115" cy="314" rx="28" ry="15" fill="#f2a516" stroke="#2b2250" stroke-width="5"/><ellipse cx="185" cy="314" rx="28" ry="15" fill="#f2a516" stroke="#2b2250" stroke-width="5"/>
    <ellipse cx="52" cy="232" rx="16" ry="26" transform="rotate(25 52 232)" fill="#ffc93c" stroke="#2b2250" stroke-width="5"/>
    <g class="qb-arm"><ellipse cx="248" cy="232" rx="16" ry="26" transform="rotate(-25 248 232)" fill="#ffc93c" stroke="#2b2250" stroke-width="5"/></g>
    <defs><clipPath id="qbclip"><circle cx="150" cy="210" r="100"/></clipPath><radialGradient id="qbskin" cx="40%" cy="35%" r="75%"><stop offset="0" stop-color="#ffe07a"/><stop offset=".6" stop-color="#ffc93c"/><stop offset="1" stop-color="#f2a516"/></radialGradient></defs>
    <circle cx="150" cy="210" r="100" fill="url(#qbskin)"/>
    <g clip-path="url(#qbclip)"><rect x="40" y="262" width="220" height="60" fill="#e63946"/><path d="M128 262 L150 284 L172 262 Z" fill="#ffc93c"/><rect x="40" y="300" width="220" height="7" fill="#fff"/></g>
    <circle cx="150" cy="210" r="100" fill="none" stroke="#2b2250" stroke-width="6"/>
    <g class="qb-eyes"><ellipse cx="118" cy="196" rx="17" ry="21" fill="#fff" stroke="#2b2250" stroke-width="4"/><ellipse cx="182" cy="196" rx="17" ry="21" fill="#fff" stroke="#2b2250" stroke-width="4"/>
    <g class="qb-pupils"><circle cx="120" cy="199" r="8" fill="#2b2250"/><circle cx="184" cy="199" r="8" fill="#2b2250"/></g></g>
    <path class="qb-mouth" d="M122 238 Q150 262 178 238" stroke="#2b2250" stroke-width="6" fill="#8a1c2b" stroke-linecap="round"/></g></svg>`;

  const groupHtml = groups.map((group, g) => `<section class="group" data-g="${g}">
      <div class="count">{{count-${g}}}</div><div class="q">{{q-${g}}}</div>
      <div class="opts">${group.options.map((_, o) => `<div class="opt" data-o="${o}"><span class="letter">{{l-${g}-${o}}}</span><span class="otext">{{o-${g}-${o}}}</span><span class="mark"></span></div>`).join("")}</div>
    </section>`).join("");

  const program = htmlVisual({
    html: `<div class="bg"><div class="rays"></div><div class="glow"></div></div>
      <header><div class="brand">{{brand}}</div><div class="topic">{{topic}}</div><div class="pills">${groups.map(() => "<i></i>").join("")}</div></header>
      ${hook >= 0 ? `<div class="hook"><div class="ha">{{hook-a}}</div><div class="hb">{{hook-b}}</div></div>` : ""}
      ${groupHtml}
      <div class="timer"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" class="track"/><circle cx="100" cy="100" r="86" class="ring"/></svg>
        <div class="num" data-n="3">{{n3}}</div><div class="num" data-n="2">{{n2}}</div><div class="num" data-n="1">{{n1}}</div></div>
      <div class="plus">{{plus}}</div>
      ${endCard >= 0 ? `<div class="endcard"><div class="ea">{{end-a}}</div><div class="eb">{{end-b}}</div></div>` : ""}
      <div class="flash"></div>
      <div class="qwrap">${qbit}</div>`,
    css: `:scope{background:#1b1240;overflow:hidden}
      .bg{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 30%,#4a2bb0 0%,#26176a 45%,#120a33 100%)}
      .rays{position:absolute;left:50%;top:38%;width:2600px;height:2600px;margin:-1300px 0 0 -1300px;opacity:.13;
        background:repeating-conic-gradient(from 0deg,#ffffff 0deg 6deg,transparent 6deg 18deg)}
      .glow{position:absolute;left:50%;top:40%;width:900px;height:900px;margin:-450px;border-radius:50%;background:radial-gradient(circle,#ffd40033,transparent 65%)}
      header{position:absolute;left:0;right:0;top:150px;text-align:center}
      .brand{letter-spacing:2px;text-shadow:0 6px 0 #b8860b,0 10px 24px #0008}
      .topic{display:inline-block;margin-top:14px;padding:8px 26px;border-radius:40px;background:#e63946;letter-spacing:3px}
      .pills{display:flex;justify-content:center;gap:14px;margin-top:22px}.pills i{width:70px;height:12px;border-radius:6px;background:#ffffff33}
      .pills i.done{background:#39FF14}.pills i.now{background:#FFD400}
      .hook{position:absolute;left:60px;right:60px;top:560px;text-align:center}
      .ha{letter-spacing:1px}.hb{margin-top:20px;text-shadow:0 8px 0 #b8860b,0 14px 30px #000a}
      .group{position:absolute;left:56px;right:56px;top:470px;display:none}
      .count{text-align:center;letter-spacing:4px}
      .q{margin:22px 0 46px;text-align:center;padding:38px 34px;border-radius:34px;background:#ffffff14;border:4px solid #ffffff30;box-shadow:0 14px 0 #0005}
      .opt{position:relative;display:flex;align-items:center;gap:28px;margin-bottom:28px;padding:22px 30px;border-radius:26px;background:#2f1f7a;border:4px solid #6b55e0;box-shadow:0 10px 0 #0b0626}
      .letter{flex:none;display:flex;align-items:center;justify-content:center;width:86px;height:86px;border-radius:22px;background:#FFD400}
      .otext{flex:1}.mark{position:absolute;right:26px;top:50%;width:64px;height:64px;margin-top:-32px;border-radius:50%;opacity:0}
      .opt.right{background:#0f8f3a;border-color:#39FF14}.opt.right .letter{background:#39FF14}.opt.right .mark{opacity:1;background:#39FF14}
      .opt.right .mark:after{content:"";position:absolute;left:20px;top:10px;width:16px;height:32px;border:solid #0b3d17;border-width:0 9px 9px 0;transform:rotate(45deg)}
      .opt.wrong{opacity:.38;filter:saturate(.3)}
      .timer{position:absolute;left:50%;top:1500px;width:230px;height:230px;margin-left:-115px;display:none}
      .timer svg{position:absolute;inset:0;transform:rotate(-90deg)}.track{fill:#120a33cc;stroke:#ffffff25;stroke-width:16}
      .ring{fill:none;stroke:#FFD400;stroke-width:16;stroke-linecap:round;stroke-dasharray:540.4;stroke-dashoffset:0}
      .num{position:absolute;inset:0;display:none;align-items:center;justify-content:center}
      .plus{position:absolute;right:120px;top:1400px;display:none;text-shadow:0 6px 0 #0b3d17}
      .endcard{position:absolute;left:60px;right:60px;top:600px;text-align:center;display:none}
      .ea{text-shadow:0 8px 0 #b8860b,0 14px 30px #000a}.eb{margin-top:34px;padding:26px 30px;border-radius:30px;background:#e63946;box-shadow:0 10px 0 #7a0f19}
      .flash{position:absolute;inset:0;background:#39FF14;opacity:0}
      .qwrap{position:absolute;left:40px;top:1440px;width:300px;height:380px}.qbit{width:300px;height:380px;overflow:visible}`,
    data: {
      fps: timeline.frameRate.numerator / timeline.frameRate.denominator, entrance: options.entranceFrames, total,
      hook: hook >= 0 ? rel(items[hook]!) : -1, endCard: endCard >= 0 ? rel(items[endCard]!) : -1,
      groups: groups.map(group => ({ start: group.start, reveal: group.reveal, end: group.end, correct: group.correct,
        options: group.options.map(option => rel(items[option]!)) })),
    },
    setup: `const fps=data.fps, E=data.entrance;
      const ease=t=>{t=Math.max(0,Math.min(1,t));return 1-Math.pow(1-t,3)};
      const back=t=>{t=Math.max(0,Math.min(1,t));const c=1.70158;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)};
      const rays=root.querySelector('.rays'), hook=root.querySelector('.hook'), sections=[...root.querySelectorAll('.group')];
      const pills=[...root.querySelectorAll('.pills i')], timer=root.querySelector('.timer'), ring=root.querySelector('.ring');
      const nums=[...root.querySelectorAll('.num')], plus=root.querySelector('.plus'), endcard=root.querySelector('.endcard');
      const flash=root.querySelector('.flash'), body=root.querySelector('.qb-body'), arm=root.querySelector('.qb-arm');
      const ant=root.querySelector('.qb-ant'), pupils=root.querySelector('.qb-pupils'), mouth=root.querySelector('.qb-mouth'), eyes=root.querySelector('.qb-eyes');
      const header=root.querySelector('header');
      return frame=>{
        const sec=frame/fps;
        rays.style.transform='rotate('+(sec*6)+'deg)';
        const h=ease(frame/E); header.style.opacity=String(h); header.style.transform='translateY('+(-40*(1-h))+'px)';
        const firstQ=data.groups.length?data.groups[0].start:data.total;
        if(hook){const age=frame-data.hook, out=frame-firstQ+6, vis=age>=0&&out<6;
          hook.style.display=vis?'block':'none';
          if(vis){const s=back(age/E)*(1-ease(out/6));hook.style.opacity=String(Math.min(1,s));hook.style.transform='scale('+(0.6+0.4*s+0.03*Math.sin(sec*6))+')';}}
        let mood='idle', moodAge=0, active=-1, countdown=false;
        data.groups.forEach((g,i)=>{
          const sec_=sections[i], vis=frame>=g.start&&frame<g.end;
          sec_.style.display=vis?'block':'none';
          if(pills[i]) pills[i].className=frame>=g.reveal?'done':(vis?'now':'');
          if(!vis) return;
          active=i;
          const age=frame-g.start, leave=frame-(g.end-8);
          const outT=leave>0?ease(leave/8):0;
          sec_.style.opacity=String(1-outT); sec_.style.transform='translateX('+(-900*outT)+'px)';
          const q=sec_.querySelector('.q'); const qs=back(age/E); q.style.transform='scale('+(0.7+0.3*qs)+')'; q.style.opacity=String(Math.min(1,qs*1.5));
          [...sec_.querySelectorAll('.opt')].forEach((o,k)=>{
            const oa=frame-g.options[k], p=back(oa/E);
            o.style.opacity=oa<0?'0':''; o.style.transform=oa<0?'translateX(900px)':'translateX('+(900*(1-p))+'px)';
            const revealed=frame>=g.reveal;
            o.className='opt'+(revealed?(k===g.correct?' right':' wrong'):'');
            if(revealed&&k===g.correct){const ra=frame-g.reveal;o.style.transform='scale('+(1+0.08*Math.max(0,1-ra/10)*Math.sin(ra*0.9))+')';}
          });
          const lastOpt=g.options[g.options.length-1]+E;
          if(frame>=lastOpt&&frame<g.reveal){countdown=true;mood='tense';
            const left=(g.reveal-frame)/fps, span=(g.reveal-lastOpt)/fps;
            ring.style.strokeDashoffset=String(540.4*(1-left/span));
            ring.style.stroke=left<1?'#E8322B':'#FFD400';
            const n=Math.min(3,Math.ceil(left*3/span));
            nums.forEach(el=>{const on=Number(el.dataset.n)===n;el.style.display=on?'flex':'none';
              if(on){const fr=(left*3/span)%1;el.style.transform='scale('+(1+0.35*fr*fr)+')';}});
          }
          if(frame>=g.reveal){mood='happy';moodAge=frame-g.reveal;}
        });
        timer.style.display=countdown?'block':'none';
        const lastReveal=active>=0?data.groups[active].reveal:-999, ra=frame-lastReveal;
        flash.style.opacity=ra>=0&&ra<6?String(0.35*(1-ra/6)):'0';
        plus.style.display=ra>=0&&ra<24?'block':'none';
        if(ra>=0&&ra<24){plus.style.opacity=String(1-Math.max(0,(ra-14)/10));plus.style.transform='translateY('+(-ra*5)+'px) scale('+back(ra/8)+')';}
        if(endcard){const age=frame-data.endCard;endcard.style.display=age>=0?'block':'none';
          if(age>=0){const s=back(age/E);endcard.style.opacity=String(Math.min(1,s));endcard.style.transform='scale('+(0.6+0.4*s)+')';mood='happy';moodAge=age%30;}}
        // Q-Bit
        const bob=Math.sin(sec/2.4*Math.PI*2)*6, ms=moodAge/fps;
        const jump=mood==='happy'&&ms<1?-Math.abs(Math.sin(ms/0.5*Math.PI))*34:0;
        const shake=mood==='tense'?Math.sin(frame*1.9)*2:0;
        body.setAttribute('transform','translate('+shake+' '+(bob+jump)+')');
        arm.setAttribute('transform','rotate('+(mood==='happy'&&ms<1.4?-40*Math.abs(Math.sin(ms*Math.PI*3.2)):0)+' 236 248)');
        ant.setAttribute('transform','rotate('+(Math.sin(sec/3*Math.PI*2)*8)+' 150 112)');
        pupils.setAttribute('transform','translate('+(mood==='tense'?9:0)+' '+(mood==='tense'?-4:0)+')');
        const blink=frame%Math.round(fps*4.2)<4?0.1:1; eyes.setAttribute('transform','translate(0 '+(196*(1-blink))+') scale(1 '+blink+')');
        mouth.setAttribute('d',mood==='happy'?'M118 232 Q150 280 182 232 Z':(mood==='tense'?'M128 246 Q150 236 172 246':'M122 238 Q150 262 178 238'));
      };`,
  });
  return sealVisualTrack({ id: options.id, timelineId: timeline.id, visualIr: "hypit.visual-ir@1",
    presents: [{ id: options.id, order: 0, z: 0, span: window.span,
      elements: [{ id: "quiz", kind: "program", order: 0, program,
        style: [{ name: "position", value: "absolute" }, { name: "left", value: `${within.xPx}px` },
          { name: "top", value: `${within.yPx}px` },
          { name: "width", value: `${within.widthPx}px` }, { name: "height", value: `${within.heightPx}px` }] }, ...children] }] });
}
