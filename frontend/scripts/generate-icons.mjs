/**
 * Generates the app's image assets from the new brand: the 间 mark in white on
 * the green→teal gradient (matching the login brand badge).
 *
 * Run from the frontend/ directory:  node scripts/generate-icons.mjs
 * Requires the devDependency @resvg/resvg-js and a CJK font (Microsoft YaHei).
 */
import { Resvg } from '@resvg/resvg-js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, '..', 'assets', 'images');
const FONT = 'C:/Windows/Fonts/msyhbd.ttc'; // Microsoft YaHei Bold

const GREEN = '#2E9E5B';
const TEAL = '#1FA8A0';
const CHAR = '间';

const grad = `<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="${GREEN}"/><stop offset="1" stop-color="${TEAL}"/>
</linearGradient></defs>`;

const glyph = (cx, cy, fs) =>
  `<text x="${cx}" y="${cy}" font-family="Microsoft YaHei" font-weight="700" font-size="${fs}" ` +
  `fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">${CHAR}</text>`;

/** Full-bleed gradient square with a centered glyph (iOS icon, Android foreground). */
function fullBleed(size, fontSize) {
  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
${grad}
<rect width="${size}" height="${size}" fill="url(#g)"/>
${glyph(size / 2, size / 2, fontSize)}
</svg>`;
}

/** Rounded gradient badge on a transparent canvas (splash, favicon). */
function badge(size, fontSize, pad) {
  const b = size - pad * 2;
  const r = b * 0.24;
  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
${grad}
<rect x="${pad}" y="${pad}" width="${b}" height="${b}" rx="${r}" fill="url(#g)"/>
${glyph(size / 2, size / 2, fontSize)}
</svg>`;
}

function render(svg, width) {
  const r = new Resvg(svg, {
    fitTo: { mode: 'width', value: width },
    font: { fontFiles: [FONT], loadSystemFonts: true, defaultFontFamily: 'Microsoft YaHei' },
  });
  return r.render().asPng();
}

const assets = [
  ['icon.png', fullBleed(1024, 520), 1024],
  ['adaptive-icon.png', fullBleed(1024, 470), 1024], // smaller glyph stays in Android safe zone
  ['splash-image.png', badge(512, 250, 24), 512],
  ['favicon.png', badge(256, 132, 10), 256],
];

for (const [name, svg, width] of assets) {
  fs.writeFileSync(path.join(OUT, name), render(svg, width));
  console.log('wrote', name);
}
