setImmediate(() => {
  const pat = "54 65 78 74 53 74 72 69 6e 67 00 00 03 31 31 39";
  const ranges = Process.enumerateRanges("rw-").filter((r) => r.size <= 0x4000000);
  const found = [];
  for (const r of ranges) {
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, pat); } catch (e) { continue; }
    for (const h of hits) found.push(h.address);
    if (found.length > 6) break;
  }
  send("found " + found.length + " " + found.join(","));
  found.forEach((f) => send("at " + f + " -> " + f.add(13).readCString(12)));
  send("done");
});
send("ready");
