const m = Process.findModuleByName("libcandycrushsaga.so");
const body = [0x00, 0x4c, 0x9d, 0x52, 0xc0, 0x03, 0x5f, 0xd6]; // mov w0,#60000 ; ret
for (const off of [0x20f5a28, 0x20f5a30]) {
  const p = m.base.add(off);
  Memory.protect(p, 8, "rwx");
  p.writeByteArray(body);
  send("patched " + off.toString(16));
}
send("done");
