// Baut story.svml aus lines.json + timings.json (Zeiten aus der echten Sprachaufnahme).
import { readFileSync, writeFileSync } from "node:fs";
const [cfgPath, timPath, outPath] = process.argv.slice(2);
const cfg = JSON.parse(readFileSync(cfgPath, "utf8")), tim = JSON.parse(readFileSync(timPath, "utf8"));
const a = s => s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const inst = cfg.lines.map((_, i) => `    <time:Instant id="l${i}" at="${tim.starts[i].toFixed(3)}s"/>`).join("\n");
const items = cfg.lines.map((l, i) => `    <story:Item id="i${i}" kind="${l.kind ?? "line"}" text="${a(l.caption ?? l.text)}" visual="${a(l.visual)}" at={show.l${i}}/>`).join("\n");
writeFileSync(outPath, `<?svml using="@hypit/markup@1"?>
<svml>
  <import as="time" from="@hypit/timeline-author@1"/>
  <import as="spatial" from="@hypit/spatial@1"/>
  <import as="media" from="@hypit/media@1"/>
  <import as="fonts" from="@hypit/fontsource@1"/>
  <import as="story" from="@cyp/story-scene@1"/>
  <import as="film" from="@hypit/film@1"/>
  <import as="html" from="@hypit/html-video@1"/>
  <import as="style" source="./story.svs"/>
  <time:Clock id="clock" frame-rate="30"/>
  <time:Timeline id="show" clock={clock} end="${tim.end.toFixed(3)}s">
${inst}
  </time:Timeline>
  <spatial:Canvas id="canvas" width="1080" height="1920"/>
  <fonts:Face id="font-face" package="@fontsource-variable/montserrat" weight="800" style="normal"/>
  <media:FontStack id="font" primary={font-face}/>
  <story:Scene id="tale" timeline={show.timeline} within={canvas.bounds} font={font} during={show.window} title="${a(cfg.title)}" entrance-frames="10">
${items}
  </story:Scene>
  <film:Film id="main" canvas={canvas.canvas} timeline={show.timeline} appearance={style.film.main}>
    <film:Track source={tale.visual}/>
  </film:Film>
  <html:Video id="final" composition={main.composition} timeline={show.timeline}/>
</svml>
`);
