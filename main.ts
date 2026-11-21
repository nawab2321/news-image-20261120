const { mkdirSync, readFileSync, writeFileSync } = require('node:fs');
const { join, resolve } = require('node:path');

const frontPage = readFileSync(join(__dirname, 'assets', 'world-in-one-page.png'));
const pngSignature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);

if (frontPage.length > 1_048_576) {
  throw new RangeError('The newspaper artwork exceeds 1 MiB.');
}

const hasImageHeader = frontPage.length >= 33 &&
  frontPage.subarray(0, 8).equals(pngSignature) &&
  frontPage.readUInt32BE(8) === 13 &&
  frontPage.toString('ascii', 12, 16) === 'IHDR';

if (!hasImageHeader || frontPage.readUInt32BE(16) !== 1024 || frontPage.readUInt32BE(20) !== 1024) {
  throw new Error('Expected a 1024 × 1024 PNG for the newspaper artwork.');
}

const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const entryPath = resolve(outputDirectory, 'entry.png');
mkdirSync(outputDirectory, { recursive: true });
writeFileSync(entryPath, frontPage);
