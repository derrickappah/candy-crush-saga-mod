setImmediate(() => {
  const pat = "54 65 78 74 53 74 72 69 6e 67 00 00";
  const ranges = Process.enumerateRanges("rw-").filter((r) => r.size <= 0x4000000);
  let shown = 0;
  for (const r of ranges) {
    let hits = [];
    try { hits = Memory.scanSync(r.base, r.size, pat); } catch (e) { continue; }
    for (const h of hits) {
      const tail = Array.from(new Uint8Array(h.address.add(12).readByteArray(8)))
        .map((x) => x.toString(16).padStart(2, "0")).join(" ");
      let asc = "";
      try { asc = h.address.add(14).readCString(10); } catch (e) {}
      send(h.address + " tail=[" + tail + "] text=[" + asc + "]");
      if (++shown > 14) { send("done"); return; }
    }
  }
  send("done " + shown);
});
send("ready");
