// Entry point for the news-image-20261125 bounty.
//
// The finished poster lives in this same directory as entry.png. This
// script only checks that the file is a valid PNG of the expected size
// and copies it, byte for byte, into the output directory. It uses the
// Node standard library only and never touches the network.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
// Last 12 bytes of every complete PNG: zero-length IEND chunk + its CRC.
const PNG_TAIL = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);
const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;

function fail(message: string): never {
  throw new Error(`entry.png failed validation: ${message}`);
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(here, "entry.png");
  if (!existsSync(sourcePath)) {
    fail(`not found at ${sourcePath}`);
  }

  const bytes = readFileSync(sourcePath);

  if (bytes.length < 33) {
    fail(`only ${bytes.length} bytes, too short to hold a PNG header`);
  }
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    fail("missing PNG signature bytes 89 50 4E 47 0D 0A 1A 0A");
  }
  if (!bytes.subarray(bytes.length - PNG_TAIL.length).equals(PNG_TAIL)) {
    fail("missing IEND trailer, the file looks truncated");
  }
  if (bytes.length >= MAX_BYTES) {
    fail(`${bytes.length} bytes, must stay under 1 MiB`);
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    fail(`dimensions ${width}x${height}, each side must be at most 1024`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR || here;
  mkdirSync(outDir, { recursive: true });
  const targetPath = join(outDir, "entry.png");
  copyFileSync(sourcePath, targetPath);
  console.log(`copied entry.png (${width}x${height}, ${bytes.length} bytes) to ${targetPath}`);
}

main();
