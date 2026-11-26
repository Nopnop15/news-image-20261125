// The World in One Page — Wednesday 25 November 2026 (full-day edition).
//
// The front page is drawn by generate_image.py and saved beside this file
// as entry.png. This program places those exact bytes at the output path
// the grader reads: MAKEFUN_OUTPUT_DIR/entry.png, or ./out/entry.png.
//
//   python3 generate_image.py
//   MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const source = join(root, "entry.png");
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(root, "out");

if (!existsSync(source)) {
  throw new Error("entry.png is missing — run python3 generate_image.py first");
}
mkdirSync(targetDir, { recursive: true });
copyFileSync(source, join(targetDir, "entry.png"));
console.log("entry.png -> " + join(targetDir, "entry.png"));
