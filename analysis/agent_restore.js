const m = Process.findModuleByName("libcandycrushsaga.so");
for (const [off, hex] of [[0x20f5a28, "001440b9c0035fd6"], [0x20f5a30, "001840b9c0035fd6"]]) {
  const p = m.base.add(off);
  Memory.protect(p, 8, "rwx");
  p.writeByteArray(hex.match(/../g).map((h) => parseInt(h, 16)));
}
send("restored");
