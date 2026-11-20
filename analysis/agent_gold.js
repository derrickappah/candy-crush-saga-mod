const m = Process.findModuleByName("libcandycrushsaga.so");
// mov w1, #60000  (0x529D4C01) over the two balance loads in the publish routine
const bytes = [0x01, 0x4c, 0x9d, 0x52];
for (const off of [0x20f58cc, 0x20f58d8]) {
  const p = m.base.add(off);
  Memory.protect(p, 4, "rwx");
  p.writeByteArray(bytes);
  send("patched " + off.toString(16) + " -> " +
       Array.from(new Uint8Array(p.readByteArray(4))).map((x) => x.toString(16)).join(" "));
}
send("done");
