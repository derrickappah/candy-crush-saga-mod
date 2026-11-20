const m = Process.findModuleByName("libcandycrushsaga.so");
const A = [0x3b15c38, 0x2e85924, 0x48067c0, 0x3b15d54];
for (const off of A) {
  const p = m.base.add(off);
  const b = Array.from(new Uint8Array(p.readByteArray(8)));
  send(off.toString(16) + " was " + b.map((x) => x.toString(16)).join(" "));
  Memory.protect(p, 8, "rwx");
  p.writeByteArray([0x00, 0x4c, 0x9d, 0x52, 0xc0, 0x03, 0x5f, 0xd6]);
}
send("done");
