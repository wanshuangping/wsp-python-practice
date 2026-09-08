const fs = require("fs");
const path = require("path");
const PptxGen = require("pptxgenjs");

const SRC = "/Users/temu/.workbuddy/clipboard-images";
const OUT = "/Users/temu/WorkBuddy/2026-08-20-01-41-58/outputs/中国办公智能体市场洞察_图片版.pptx";

// Read PNG intrinsic size from the IHDR chunk.
function pngSize(p) {
  const buf = fs.readFileSync(p);
  if (buf.toString("ascii", 1, 4) !== "PNG") return { w: 1280, h: 720 };
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

const files = fs.readdirSync(SRC)
  .filter((f) => /\.png$/i.test(f) && f.includes("2026-08-20T08-42-00"))
  .sort();
console.log("Found images:", files.length);

const pres = new PptxGen();
pres.defineLayout({ name: "W16x9", width: 10, height: 5.625 });
pres.layout = "W16x9";
pres.author = "WorkBuddy";
pres.title = "中国办公智能体市场洞察（图片版）";

const M = 0.22; // margin inch
const pageW = 10, pageH = 5.625;

files.forEach((f, i) => {
  const slide = pres.addSlide();
  slide.background = { color: "FFFFFF" };
  const full = path.join(SRC, f);
  const sz = pngSize(full);
  const aw = pageW - 2 * M;
  const ah = pageH - 2 * M;
  const scale = Math.min(aw / sz.w, ah / sz.h);
  const w = sz.w * scale;
  const h = sz.h * scale;
  const x = (pageW - w) / 2;
  const y = (pageH - h) / 2;
  slide.addImage({ path: full, x, y, w, h });
  slide.addText(`${i + 1} / ${files.length}`, {
    x: pageW - 1.2, y: pageH - 0.34, w: 1.0, h: 0.28,
    fontSize: 9, fontFace: "Arial", color: "9CA3AF", align: "right",
  });
});

pres.writeFile({ fileName: OUT }).then(() => {
  console.log("Saved:", OUT);
}).catch((e) => {
  console.error("ERROR:", e);
  process.exit(1);
});
