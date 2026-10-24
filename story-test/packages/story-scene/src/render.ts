import { sealVisualTrack } from "@hypit/composition";
import type { VisualElement } from "@hypit/composition";
import { htmlVisual } from "@hypit/html-program";
import type { FontStackRef } from "@hypit/media";
import type { Timeline } from "@hypit/timeline";
import type { SpatialFrame } from "@hypit/spatial";
import { assertTemporalWindowFor } from "@hypit/temporal";
import type { TemporalInstant, TemporalWindow } from "@hypit/temporal";

export type Message = { id: string; kind: "line" | "end"; text: string; visual: string; at: TemporalInstant };
export type StoryOptions = { id: string; title: string; entranceFrames: number };

const CAP = `<svg class="ico" viewBox="0 0 120 90"><path d="M60 8 L116 32 L60 56 L4 32 Z" fill="#f5c542"/><path d="M28 44 V66 Q60 84 92 66 V44 L60 58 Z" fill="#d9a521"/><path d="M104 36 V68" stroke="#f5c542" stroke-width="5"/><circle cx="104" cy="72" r="6" fill="#f5c542"/></svg>`;
const CASE = `<svg class="ico" viewBox="0 0 120 90"><rect x="40" y="8" width="40" height="20" rx="6" fill="none" stroke="#f5c542" stroke-width="7"/><rect x="8" y="24" width="104" height="60" rx="10" fill="#f5c542"/><rect x="8" y="46" width="104" height="6" fill="#b88a12"/><rect x="52" y="42" width="16" height="14" rx="3" fill="#7a5a08"/></svg>`;
const HEART = `<svg class="ico" viewBox="0 0 120 100"><path d="M60 92 C10 58 4 34 18 18 C32 2 54 8 60 26 C66 8 88 2 102 18 C116 34 110 58 60 92 Z" fill="#e8475f"/></svg>`;
const ICONS: Record<string, string> = { cap: CAP, case: CASE, heart: HEART };

/** One spoken line → one visual beat plus its caption chunks. Times arrive resolved from the narration. */
export function renderStory(timeline: Timeline, within: SpatialFrame, window: TemporalWindow,
  font: FontStackRef, lines: readonly Message[], options: StoryOptions) {
  assertTemporalWindowFor(window, { subjectId: options.id, timeline });
  if (lines.some(line => line.at.frame < window.span.startFrame || line.at.frame >= window.span.endFrameExclusive)) throw new Error("Story lines must start inside the scene's window.");
  const total = window.span.endFrameExclusive - window.span.startFrame;
  const starts = lines.map(line => line.at.frame - window.span.startFrame);

  let order = 0;
  const els: VisualElement[] = [];
  const text = (id: string, value: string, size: number, color: string, extra: { name: string; value: string | number }[] = []) => {
    els.push({ id, kind: "text", parent: "story", order: ++order, text: value, fonts: font.faces,
      style: [{ name: "font-size", value: `${size}px` }, { name: "line-height", value: 1.08 }, { name: "color", value: color }, ...extra] });
    return `{{${id}}}`;
  };
  text("brand", options.title.toUpperCase(), 30, "#f5c542", [{ name: "letter-spacing", value: "8px" }]);

  // Degrees collect on a shelf as the story earns them.
  const earned: { name: string; year: string; start: number }[] = [];
  const beats: string[] = [];
  const caps: { line: number; start: number; end: number }[] = [];

  lines.forEach((line, i) => {
    const start = starts[i]!, end = starts[i + 1] ?? total;
    const [type, a = "", b = "", c = ""] = line.visual.split("|");
    let inner = "";
    if (type === "money") {
      const formatted = "$" + Number(a).toLocaleString("en-US");
      let slots = "", d = 0;
      for (const ch of formatted) {
        if (/\d/.test(ch)) { slots += `<span class="slot"><span class="reel" data-digit="${ch}" data-k="${d}">${text(`m${i}-${d}`, "0 1 2 3 4 5 6 7 8 9", 128, "#f5c542", [{ name: "line-height", value: 1 }])}</span></span>`; d++; }
        else slots += `<span class="sep">${text(`m${i}-s${slots.length}`, ch, 128, "#f5c542", [{ name: "line-height", value: 1 }])}</span>`;
      }
      inner = `<div class="money">${slots}</div><div class="label">${text(`l${i}`, b, 34, "#cfd6e6", [{ name: "letter-spacing", value: "4px" }])}</div>`;
    } else if (type === "quote") {
      inner = `<div class="quote"><div class="qmark">${text(`qm${i}`, "“", 220, "#f5c542")}</div>${text(`q${i}`, a, 70, "#ffffff")}<div class="who">${text(`qw${i}`, "— " + b, 36, "#f5c542", [{ name: "letter-spacing", value: "4px" }])}</div></div>`;
    } else if (type === "degree") {
      earned.push({ name: a, year: b, start });
      inner = `<div class="degree">${CAP}<div class="dname">${text(`d${i}`, a, 150, "#ffffff")}</div><div class="label">${text(`dy${i}`, `${c} · ${b}`, 40, "#f5c542", [{ name: "letter-spacing", value: "5px" }])}</div></div>`;
    } else if (type === "stamp") {
      inner = `<div class="stamp">${text(`st${i}`, a, 150, "#e8475f")}</div><div class="label">${text(`l${i}`, b, 38, "#cfd6e6", [{ name: "letter-spacing", value: "4px" }])}</div>`;
    } else if (type === "name") {
      inner = `<div class="plate"><div class="pname">${text(`n${i}`, a, 110, "#1a1408")}</div></div><div class="label">${text(`l${i}`, b, 36, "#f5c542", [{ name: "letter-spacing", value: "5px" }])}</div>`;
    } else if (type === "end") {
      inner = `<div class="endc"><div class="big">${text(`e${i}`, a, 140, "#f5c542")}</div><div class="label">${text(`l${i}`, b, 44, "#ffffff", [{ name: "letter-spacing", value: "4px" }])}</div></div>`;
    } else {
      inner = `${c && ICONS[c] ? ICONS[c] : ""}<div class="big">${text(`t${i}`, a, 112, "#ffffff")}</div>${b ? `<div class="label">${text(`l${i}`, b, 36, "#f5c542", [{ name: "letter-spacing", value: "5px" }])}</div>` : ""}`;
    }
    beats.push(`<section class="beat t-${type}" data-i="${i}">${inner}</section>`);

    if (line.kind === "line") {
      const words = line.text.split(/\s+/).filter(Boolean), chunks: string[] = [];
      for (let w = 0; w < words.length;) {
        const n = words.length - w === 4 ? 2 : Math.min(3, words.length - w);
        chunks.push(words.slice(w, w + n).join(" ")); w += n;
      }
      const totalChars = chunks.reduce((s, ch) => s + ch.length + 1, 0);
      const speak = Math.max(1, end - start - 8);
      let acc = 0;
      chunks.forEach((chunk, k) => {
        const cs = start + Math.round(speak * acc / totalChars); acc += chunk.length + 1;
        const ce = k === chunks.length - 1 ? end : start + Math.round(speak * acc / totalChars);
        const hot = /[$\d]/.test(chunk);
        text(`c${i}-${k}`, chunk.toUpperCase(), 66, hot ? "#f5c542" : "#ffffff");
        caps.push({ line: i, start: cs, end: ce });
      });
    }
  });

  const capHtml = caps.map((cap, k) => `<div class="cap" data-k="${k}">{{c${cap.line}-${caps.slice(0, k).filter(x => x.line === cap.line).length}}}</div>`).join("");
  const shelf = earned.map((deg, k) => `<div class="pill" data-k="${k}">${text(`sh${k}`, `${deg.name} · ${deg.year}`, 30, "#1a1408")}</div>`).join("");

  const program = htmlVisual({
    html: `<div class="bg"><div class="beam"></div><div class="dust"></div><div class="vig"></div></div>
      <div class="brand"><i></i>{{brand}}<i></i></div>
      <div class="shelf">${shelf}</div>
      <div class="stage">${beats.join("")}</div>
      <div class="caps">${capHtml}</div>
      <div class="bar"><div class="fill"></div></div>`,
    css: `:scope{background:#07080d;overflow:hidden}
      .bg{position:absolute;inset:0;background:radial-gradient(90% 60% at 50% 38%,#1d2a44 0%,#0c111d 55%,#05060a 100%)}
      .beam{position:absolute;left:50%;top:-200px;width:900px;height:1700px;margin-left:-450px;background:linear-gradient(180deg,#f5c54222,transparent 70%);clip-path:polygon(40% 0,60% 0,100% 100%,0 100%);filter:blur(30px)}
      .dust{position:absolute;inset:-100px;opacity:.35;background-image:radial-gradient(#f5c542 1.5px,transparent 2px),radial-gradient(#ffffff 1px,transparent 1.5px);background-size:170px 190px,110px 130px;background-position:0 0,40px 70px}
      .vig{position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 45%,transparent 55%,#000c 100%)}
      .brand{position:absolute;top:170px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:22px}
      .brand i{display:block;width:80px;height:3px;background:#f5c542}
      .shelf{position:absolute;top:250px;left:0;right:0;display:flex;justify-content:center;gap:16px}
      .pill{padding:10px 22px;border-radius:30px;background:#f5c542;opacity:0}
      .stage{position:absolute;left:70px;right:70px;top:430px;height:640px}
      .beat{position:absolute;inset:0;display:none;flex-direction:column;align-items:center;justify-content:center;text-align:center}
      .label{margin-top:28px}
      .money{display:flex;align-items:flex-start;height:128px;overflow:hidden;filter:drop-shadow(0 6px 0 #6b4c00) drop-shadow(0 0 40px #f5c54255)}
      .slot{display:block;width:86px;height:128px;overflow:hidden}.reel{display:block;width:86px;text-align:center;word-break:break-all}
      .sep{display:block;height:128px}
      .quote{position:relative;padding:40px 30px;border-left:8px solid #f5c542;background:#ffffff0d;border-radius:0 30px 30px 0;text-align:left}
      .qmark{position:absolute;left:18px;top:-120px;opacity:.9}.who{margin-top:26px}
      .ico{width:240px;height:180px;margin-bottom:24px;filter:drop-shadow(0 0 30px #f5c54266)}
      .degree .dname{filter:drop-shadow(0 8px 0 #000a)}
      .stamp{padding:10px 40px;border:12px solid #e8475f;border-radius:18px;transform:rotate(-8deg)}
      .plate{padding:34px 60px;border-radius:20px;background:linear-gradient(180deg,#ffe28a,#d9a521);box-shadow:0 12px 0 #6b4c00,0 0 80px #f5c54266}
      .big{filter:drop-shadow(0 8px 0 #000a)}
      .caps{position:absolute;left:60px;right:60px;top:1180px;height:200px}
      .cap{position:absolute;left:0;right:0;top:0;text-align:center;display:none;-webkit-text-stroke:3px #000;paint-order:stroke fill;filter:drop-shadow(0 6px 0 #000)}
      .bar{position:absolute;left:0;right:0;bottom:0;height:10px;background:#ffffff14}.fill{height:100%;width:0;background:#f5c542}`,
    data: { starts, total, entrance: options.entranceFrames, caps, earned: earned.map(d => d.start),
      kinds: lines.map(l => l.visual.split("|")[0]) },
    setup: `const E=data.entrance, starts=data.starts, total=data.total;
      const ease=t=>{t=Math.max(0,Math.min(1,t));return 1-Math.pow(1-t,3)};
      const back=t=>{t=Math.max(0,Math.min(1,t));const c=1.70158;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)};
      const beats=[...root.querySelectorAll('.beat')], caps=[...root.querySelectorAll('.cap')], pills=[...root.querySelectorAll('.pill')];
      const dust=root.querySelector('.dust'), beam=root.querySelector('.beam'), fill=root.querySelector('.fill'), stage=root.querySelector('.stage');
      return frame=>{
        dust.style.transform='translate('+(Math.sin(frame/90)*30)+'px,'+(-frame*0.6%190)+'px)';
        beam.style.opacity=String(0.7+0.3*Math.sin(frame/40));
        fill.style.width=(100*frame/total)+'%';
        stage.style.transform='scale('+(1+0.02*Math.sin(frame/60))+')';
        let cur=-1; starts.forEach((s,i)=>{if(frame>=s)cur=i;});
        beats.forEach((b,i)=>{
          const vis=i===cur||(i===cur-1&&frame-starts[cur]<6);
          b.style.display=vis?'flex':'none'; if(!vis)return;
          if(i===cur-1){const o=ease((frame-starts[cur])/6);b.style.opacity=String(1-o);b.style.transform='translateY('+(-60*o)+'px)';return;}
          const age=frame-starts[i], k=data.kinds[i];
          const p=k==='stamp'?back(age/(E*0.8)):back(age/E);
          b.style.opacity=String(Math.min(1,ease(age/E)*1.4));
          b.style.transform=k==='stamp'?'scale('+(2.2-1.2*p)+')':'translateY('+(70*(1-p))+'px) scale('+(0.92+0.08*p)+')';
          if(k==='money'){b.querySelectorAll('.reel').forEach(r=>{const target=Number(r.dataset.digit), kk=Number(r.dataset.k);
            const t=ease((age-kk*2)/36); const v=t*(20+target)%10; const pos=(t>=1?target:v);
            r.style.transform='translateY('+(-128*pos)+'px)';});}
        });
        caps.forEach((c,k)=>{const cp=data.caps[k], vis=frame>=cp.start&&frame<cp.end;
          c.style.display=vis?'block':'none'; if(vis){const p=back((frame-cp.start)/5);c.style.transform='scale('+(0.8+0.2*p)+')';}});
        pills.forEach((p,k)=>{const age=frame-data.earned[k]-20;p.style.opacity=age>=0?'1':'0';if(age>=0)p.style.transform='scale('+back(age/8)+')';});
      };`,
  });
  return sealVisualTrack({ id: options.id, timelineId: timeline.id, visualIr: "hypit.visual-ir@1",
    presents: [{ id: options.id, order: 0, z: 0, span: window.span,
      elements: [{ id: "story", kind: "program", order: 0, program,
        style: [{ name: "position", value: "absolute" }, { name: "left", value: `${within.xPx}px` },
          { name: "top", value: `${within.yPx}px` },
          { name: "width", value: `${within.widthPx}px` }, { name: "height", value: `${within.heightPx}px` }] }, ...els] }] });
}
