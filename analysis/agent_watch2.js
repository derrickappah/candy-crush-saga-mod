setImmediate(() => {
  const ranges = Process.enumerateRanges("rw-").filter((r) => r.size <= 0x4000000);
  let target = null;
  for (const r of ranges) {
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, "69 63 6f 6e 5f 67 6f 6c 64 62 61 72"); } catch (e) { continue; }
    for (const h of hits) {
      let ctx = "";
      try { ctx = h.address.sub(100).readCString(100); } catch (e) {}
      if (ctx.indexOf("SceneObject") >= 0) { target = h.address; break; }
    }
    if (target) break;
  }
  if (!target) { send("no node"); return; }
  let tsHits = [];
  try {
    tsHits = Memory.scanSync(target.sub(0x400), 0x400, "54 65 78 74 53 74 72 69 6e 67");
  } catch (e) {}
  if (!tsHits.length) { send("no textstring"); return; }
  const ts = tsHits[tsHits.length - 1].address.add(11);
  send("ts=" + ts + " value=" + ts.readCString(24));

  const page = ts.and(ptr(0x1000).not());
  const seen = {};
  MemoryAccessMonitor.enable({ base: page, size: 0x1000 }, {
    onAccess(d) {
      const a = d.address;
      if (a.compare(ts.sub(8)) < 0 || a.compare(ts.add(40)) >= 0) return;
      const bt = Thread.backtrace(this.context, Backtracer.ACCURATE).slice(0, 4);
      const key = bt.map((x) => x.toString()).join(",");
      if (seen[key]) return;
      seen[key] = 1;
      send("ACCESS " + d.operation + " at " + a + " bt=" + key);
    },
  });
  send("monitoring");
});
send("ready");
