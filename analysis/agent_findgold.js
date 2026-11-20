setImmediate(() => {
  const ranges = Process.enumerateRanges("rw-").filter((r) => r.size <= 0x4000000);
  send("ranges " + ranges.length + " total " + ranges.reduce((a, r) => a + r.size, 0));
  let out = 0;
  for (const r of ranges) {
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, "67 6f 6c 64"); } catch (e) { continue; }
    for (const h of hits) {
      let s = "";
      try { s = h.address.sub(48).readCString(140); } catch (e) {}
      if (s.length > 10) {
        send(h.address + " :: " + s.replace(/\n/g, " "));
        if (++out > 10) { send("done"); return; }
      }
    }
  }
  send("done " + out);
});
send("ready");
