setImmediate(() => {
  const out = [];
  let scanned = 0;
  const ranges = Process.enumerateRanges("rw-").filter(
    (r) => r.size >= 0x1000 && r.size <= 0x2000000);
  for (const r of ranges) {
    if (scanned > 0x12000000) break;
    scanned += r.size;
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, "46 00 75 00 6c 00 6c 00"); } catch (e) { continue; }
    for (const h of hits) {
      let near = [];
      try { near = Memory.scanSync(h.address.sub(0x4000), 0x8000, "31 00 31 00 39 00"); } catch (e) {}
      if (near.length) out.push(h.address + " " + near.slice(0, 3).map((n) => n.address).join(","));
    }
  }
  send("pairs=" + out.length + " :: " + out.slice(0, 10).join(" | "));
  send("done");
});
send("ready");
