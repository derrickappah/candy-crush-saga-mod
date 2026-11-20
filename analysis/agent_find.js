const MOD = "libcandycrushsaga.so";
const VT = Process.findModuleByName(MOD).base.add(0x4e57ab8 + 0x10);

function hexOf(p) {
  const s = p.toString().padStart(16, "0");
  let out = "";
  for (let i = 14; i >= 0; i -= 2) out += s.substr(i, 2) + " ";
  return out.trim();
}

send("vt=" + VT);
const pat = hexOf(VT);
const found = [];
const ranges = Process.enumerateRanges("rw-");
send("ranges " + ranges.length);
for (const r of ranges) {
  if (r.size > 512 * 1024 * 1024) continue;
  try {
    Memory.scanSync(r.base, r.size, pat).forEach(m => found.push(m.address));
  } catch (e) {}
}
send("instances " + found.length);
for (const a of found.slice(0, 20)) {
  send("  obj " + a + "  field9a8=" + a.add(0x9a8).readS32() + "  0x0=" + a.readPointer());
}
