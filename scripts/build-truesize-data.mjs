// Baut src/data/truesize.json: Umrisse (Natural Earth, Public Domain, via world-atlas) für das Layout "atlas"
// ("The map is lying" – echte Größen auf der Mercator-Karte). Aufruf: node scripts/build-truesize-data.mjs
import {createRequire} from 'node:module';
import {writeFileSync} from 'node:fs';
import {feature, merge} from 'topojson-client';
import {geoArea, geoCentroid} from 'd3-geo';
const require = createRequire(import.meta.url);
const w50 = require('world-atlas/countries-50m.json');
const w110 = require('world-atlas/countries-110m.json');
const R2 = 6371.0088 ** 2;

const NOT_AFRICA = new Set(['Yemen', 'United Arab Emirates', 'Syria', 'Saudi Arabia', 'Qatar', 'Oman', 'Malta', 'Lebanon', 'Kuwait', 'Jordan', 'Israel', 'Palestine', 'Iraq', 'Iran', 'N. Cyprus', 'Cyprus', 'Bahrain', 'Saint Helena', 'Seychelles', 'Mauritius', 'Comoros', 'Cabo Verde', 'São Tomé and Principe']);
const geoms = w50.objects.countries.geometries;
const byName = (n) => feature(w50, geoms.find((g) => g.properties.name === n));
const africa = () => {
  const gs = geoms.filter((g) => {
    if (NOT_AFRICA.has(g.properties.name)) return false;
    const c = geoCentroid(feature(w50, g));
    return c[0] > -26 && c[0] < 60 && c[1] > -36 && c[1] < 38;
  });
  return {type: 'Feature', properties: {name: 'Africa'}, geometry: merge(w50, gs)};
};

const r2 = (v) => Math.round(v * 100) / 100;
/** Alle Außenringe als [[lon,lat],…]; Mini-Inseln (< minKm2) fallen weg */
const rings = (f, minKm2) => {
  const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  const out = [];
  for (const p of polys) {
    const a = geoArea({type: 'Polygon', coordinates: [p[0]]}) * R2;
    if (a < minKm2) continue;
    out.push(p[0].map(([x, y]) => [r2(x), r2(y)]));
  }
  return out;
};
const shape = (f, minKm2 = 400) => {
  const rs = rings(f, minKm2);
  // Schwerpunkt nur aus den behaltenen Ringen (stabil, ohne ferne Inseln)
  const c = geoCentroid({type: 'MultiPolygon', coordinates: rs.map((r) => [r])});
  return {rings: rs, centroid: [r2(c[0]), r2(c[1])]};
};

const us10 = require('us-atlas/states-10m.json');
const stateByName = (n) => feature(us10, us10.objects.states.geometries.find((g) => g.properties.name === n));
/** Nur Ringe, deren Schwerpunkt im Kasten [lon0, lat0, lon1, lat1] liegt (z. B. Frankreich ohne Übersee) */
const clip = (f, [x0, y0, x1, y1]) => {
  const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  const keep = polys.filter((p) => {
    const c = geoCentroid({type: 'Polygon', coordinates: [p[0]]});
    return c[0] >= x0 && c[0] <= x1 && c[1] >= y0 && c[1] <= y1;
  });
  return {type: 'Feature', properties: f.properties, geometry: {type: 'MultiPolygon', coordinates: keep}};
};

const data = {
  shapes: {
    greenland: shape(byName('Greenland'), 2000),
    australia: shape(byName('Australia'), 3000),
    russia: shape(byName('Russia'), 3000),
    africa: shape(africa(), 3000),
    sweden: shape(byName('Sweden'), 150),
    madagascar: shape(byName('Madagascar'), 150),
    congo: shape(byName('Dem. Rep. Congo'), 500),
    china: shape(byName('China'), 3000),
    canada: shape(byName('Canada'), 6000),
    brazil: shape(byName('Brazil'), 3000),
    india: shape(byName('India'), 2000),
    mexico: shape(byName('Mexico'), 1500),
    alaska: shape(clip(stateByName('Alaska'), [-170, 50, -128, 73]), 3000),
    texas: shape(stateByName('Texas'), 1000),
    uk: shape(clip(byName('United Kingdom'), [-9, 49, 3, 61]), 400),
    philippines: shape(byName('Philippines'), 1200),
    japan: shape(byName('Japan'), 800),
    germany: shape(byName('Germany'), 300),
    iceland: shape(byName('Iceland'), 300),
    cuba: shape(byName('Cuba'), 300),
    spain: shape(clip(byName('Spain'), [-10, 35, 5, 44]), 600),
    finland: shape(byName('Finland'), 300),
    italy: shape(byName('Italy'), 300),
    newzealand: shape(clip(byName('New Zealand'), [165, -48, 179, -33]), 800),
    france: shape(clip(byName('France'), [-6, 41, 10, 52]), 300),
    kazakhstan: shape(byName('Kazakhstan'), 1000),
    algeria: shape(byName('Algeria'), 1000),
    iran: shape(byName('Iran'), 1000),
    mongolia: shape(byName('Mongolia'), 1000),
    peru: shape(byName('Peru'), 1000),
    svalbard: shape(clip(byName('Norway'), [5, 74, 35, 82]), 300),
    srilanka: shape(byName('Sri Lanka'), 300),
    ukraine: shape(byName('Ukraine'), 500),
    california: shape(stateByName('California'), 300),
    florida: shape(stateByName('Florida'), 300),
    minnesota: shape(stateByName('Minnesota'), 300),
    colorado: shape(stateByName('Colorado'), 300),
    utah: shape(stateByName('Utah'), 300),
    nevada: shape(stateByName('Nevada'), 300),
    montana: shape(stateByName('Montana'), 300),
    pennsylvania: shape(stateByName('Pennsylvania'), 300),
    turkey: shape(byName('Turkey'), 300),
    syria: shape(byName('Syria'), 300),
    romania: shape(byName('Romania'), 300),
    chile: shape(clip(byName('Chile'), [-76, -56, -66, -17]), 300),
    cambodia: shape(byName('Cambodia'), 300),
    poland: shape(byName('Poland'), 300),
    norway: shape(clip(byName('Norway'), [4, 57, 32, 72]), 300),
  },
  world: feature(w110, w110.objects.countries).features
    .filter((f) => f.properties.name !== 'Antarctica')
    .flatMap((f) => rings(f, 1500)),
};
// Kontrolle: Fläche der behaltenen Ringe (Kugel) – muss grob zur offiziellen Fläche passen
for (const [k, v] of Object.entries(data.shapes)) v._km2 = Math.round(geoArea({type: 'MultiPolygon', coordinates: v.rings.map((r) => [r])}) * R2);
writeFileSync(new URL('../src/data/truesize.json', import.meta.url), JSON.stringify(data));
for (const [k, v] of Object.entries(data.shapes)) console.log(k.padEnd(12), String(v.rings.length).padStart(3), 'Ringe', String(v.rings.reduce((s, r) => s + r.length, 0)).padStart(6), 'Punkte', String(v._km2).padStart(9), 'km²', v.centroid);
console.log('world', data.world.length, 'Ringe');
