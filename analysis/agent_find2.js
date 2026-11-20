const m = Process.findModuleByName("libcandycrushsaga.so");
const vts = [0x4e57ab8, 0x4e57d80, 0x4e57db0, 0x4e57de0, 0x4e57e08, 0x4e57e30, 0x4e57e70, 0x4e57e98, 0x4e57ec0, 0x4e57ee8, 0x4e57f18];

const scratch = Memory.alloc(8);
function patFor(p) {
  scratch.writePointer(p);
  const b = new Uint8Array(scratch.readByteArray(8));
  return Array.from(b).map(x => x.toString(16).padStart(2, "0")).join(" ");
}

const pats = vts.map(o => patFor(m.base.add(o + 0x10)));
send("patterns " + pats.join(" | "));

const ranges = Process.enumerateRanges("rw-").filter(r => r.size < 256 * 1024 * 1024);
send("ranges " + ranges.length);
let total = 0;
for (const pat of pats) {
  const hits = [];
  for (const r of ranges) {
    try {
      Memory.scanSync(r.base, r.size, pat).forEach(h => hits.push(h.address));
    } catch (e) {}
  }
  send("pat " + pat + " -> " + hits.length);
  for (const h of hits.slice(0, 6)) {
    send("   at " + h + "  9a8=" + h.add(0x9a8).readS32() + " 9e0=" + h.add(0x9e0).readS32());
  }
  total += hits.length;
}
send("total " + total);
