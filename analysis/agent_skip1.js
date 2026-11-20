const m = Process.findModuleByName("libcandycrushsaga.so");
function put(off, hex) {
  const p = m.base.add(off);
  Memory.protect(p, 8, "rwx");
  p.writeByteArray(hex.match(/../g).map((h) => parseInt(h, 16)));
}
put(0x2a031b4, "20008052c0035fd6"); // mov w0,#1 ; ret
put(0x2abb69c, "1f2003d5");
send("one armed");
