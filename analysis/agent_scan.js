const m = Process.findModuleByName("libcandycrushsaga.so");

function hexOf(addr) {
  const p = Memory.alloc(8);
  p.writePointer(addr);
  return Array.from(new Uint8Array(p.readByteArray(8)))
    .map((x) => ("0" + x.toString(16)).slice(-2)).join(" ");
}

function count(addr) {
  const hex = hexOf(addr);
  let total = 0, faults = 0;
  for (const r of Process.enumerateRanges("rw-")) {
    try { total += Memory.scanSync(r.base, r.size, hex).length; } catch (e) { faults++; }
  }
  return total + "/" + faults;
}

send("ranges=" + Process.enumerateRanges("rw-").length);
send("gameState=" + count(m.base.add(0x4e57ab8)));
send("invModel=" + count(m.base.add(0x4ddd1b0)));
send("invModel2=" + count(m.base.add(0x4ddd250)));
send("updater=" + count(m.base.add(0x4dba3b8)));
