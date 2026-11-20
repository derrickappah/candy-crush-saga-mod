setImmediate(() => {
  const ranges = Process.enumerateRanges("rw-").filter((r) => r.size <= 0x4000000);
  let node = null;
  outer:
  for (const r of ranges) {
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, "69 63 6f 6e 5f 67 6f 6c 64 62 61 72"); } catch (e) { continue; }
    for (const h of hits) {
      let ctx = "";
      try { ctx = h.address.sub(120).readCString(120); } catch (e) {}
      if (ctx.indexOf("SceneObject") >= 0) { node = h.address; break outer; }
    }
  }
  if (!node) { send("no node"); return; }
  send("node " + node);
  const start = node.sub(0x800);
  let hits = [];
  try { hits = Memory.scanSync(start, 0x1000, "54 65 78 74 53 74 72 69 6e 67"); } catch (e) {}
  send("textstrings " + hits.length);
  for (const h of hits) {
    let v = "";
    try { v = h.address.add(11).readCString(20); } catch (e) {}
    send(h.address + " value=[" + v + "] dist=" + h.address.sub(node));
  }
  send("done");
});
send("ready");
