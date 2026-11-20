setImmediate(() => {
  const ranges = Process.enumerateRanges("rw-").filter((r) => r.size <= 0x4000000);
  for (const r of ranges) {
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, "69 63 6f 6e 5f 67 6f 6c 64 62 61 72"); } catch (e) { continue; }
    for (const h of hits) {
      let s = "";
      try { s = h.address.sub(0x300).readCString(0x1400); } catch (e) {}
      send("AT " + h.address + " :: " + s.replace(/[\x00-\x08\x0b-\x1f]/g, "."));
    }
  }
  send("done");
});
send("ready");
