const { copyFileSync, mkdirSync } = require('node:fs');
const { join, resolve } = require('node:path');

const cover = join(__dirname, 'entry.png');
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const entryPath = resolve(outputDirectory, 'entry.png');

mkdirSync(outputDirectory, { recursive: true });
copyFileSync(cover, entryPath);
