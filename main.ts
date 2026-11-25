// News-image entry for Wednesday 25 November 2026.
//
// The poster is drawn ahead of time and committed next to this file as
// entry.png. This program only inspects that file and copies it into the
// output directory, so the grader's two runs write identical bytes.
// Node 22, standard library only, no network.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? here;

function fail(message: string): never {
  throw new Error(`entry.png failed its checks: ${message}`);
}

if (!existsSync(source)) {
  fail("the file is missing");
}
const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  fail(`it is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  fail("it is not a PNG file");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  fail(`it is ${width}x${height}, over the 1024x1024 limit`);
}

const dest = join(outDir, "entry.png");
if (resolve(dest) !== resolve(source)) {
  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, dest);
}
