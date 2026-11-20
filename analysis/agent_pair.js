const m = Process.findModuleByName("libcandycrushsaga.so");
const orig = {
  "0x3b15c38": "001840b9c0035fd6",
  "0x2e85924": "001840b9c0035fd6",
  "0x48067c0": "001840b9c0035fd6",
  "0x3b15d54": "001440b9c0035fd6",
};
const targets = [0x3b15c38, 0x3b15d54];
for (const k in orig) {
  const p = m.base.add(Number(k));
  Memory.protect(p, 8, "rwx");
  p.writeByteArray(orig[k].match(/../g).map((h) => parseInt(h, 16)));
}
for (const t of targets) {
  const q = m.base.add(t);
  Memory.protect(q, 8, "rwx");
  q.writeByteArray([0x00, 0x4c, 0x9d, 0x52, 0xc0, 0x03, 0x5f, 0xd6]);
}
send("expair " + targets.length);
send("done");
