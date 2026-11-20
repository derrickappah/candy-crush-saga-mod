const m = Process.findModuleByName("libcandycrushsaga.so");
const p = Memory.alloc(8);
function hexOf(addr) {
  p.writePointer(addr);
  return Array.from(new Uint8Array(p.readByteArray(8)))
    .map((x) => ("0" + x.toString(16)).slice(-2)).join(" ");
}
function count(addr) {
  const hex = hexOf(addr);
  let n = 0;
  for (const r of Process.enumerateRanges("rw-")) {
    try { n += Memory.scanSync(r.base, r.size, hex).length; } catch (e) {}
  }
  return n;
}
send("strBoostersCount=" + count(m.base.add(0x9516f7)));
send("strInvAmount=" + count(m.base.add(0x8c3cab)));
send("vtGame=" + count(m.base.add(0x4e57ab8)));
send("vtInv=" + count(m.base.add(0x4ddd1b0)));
send("moduleBase=" + m.base + " size=" + m.size);
