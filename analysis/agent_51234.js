const m = Process.findModuleByName("libcandycrushsaga.so");
const body = [0x40, 0x04, 0x9c, 0x52, 0xc0, 0x03, 0x5f, 0xd6]; // mov w0,#51234 ; ret
for (const off of [0x20f5a28, 0x20f5a30]) {
  const p = m.base.add(off);
  Memory.protect(p, 8, "rwx");
  p.writeByteArray(body);
}
send("patched51234");
