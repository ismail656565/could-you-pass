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

const data = {
  shapes: {
    greenland: shape(byName('Greenland'), 2000),
    australia: shape(byName('Australia'), 3000),
    russia: shape(byName('Russia'), 3000),
    africa: shape(africa(), 3000),
    sweden: shape(byName('Sweden'), 150),
    madagascar: shape(byName('Madagascar'), 150),
    congo: shape(byName('Dem. Rep. Congo'), 500),
  },
  world: feature(w110, w110.objects.countries).features
    .filter((f) => f.properties.name !== 'Antarctica')
    .flatMap((f) => rings(f, 1500)),
};
writeFileSync(new URL('../src/data/truesize.json', import.meta.url), JSON.stringify(data));
for (const [k, v] of Object.entries(data.shapes)) console.log(k, v.rings.length, 'Ringe', v.rings.reduce((s, r) => s + r.length, 0), 'Punkte', v.centroid);
console.log('world', data.world.length, 'Ringe');
