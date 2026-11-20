setImmediate(() => {
  const pat = "00 00 01 31 31 39";
  const ranges = Process.enumerateRanges("rw-").filter((r) => r.size <= 0x4000000);
  let shown = 0;
  for (const r of ranges) {
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, pat); } catch (e) { continue; }
    for (const h of hits) {
      let ctx = "";
      try { ctx = h.address.sub(40).readCString(40); } catch (e) {}
      send(h.address + " ctx=[" + ctx.replace(/[^\x20-\x7e]/g, ".") + "]");
      if (++shown > 12) { send("done"); return; }
    }
  }
  send("done " + shown);
});
send("ready");
