const m = Process.findModuleByName("libcandycrushsaga.so");
function rd(off, n) {
  const b = m.base.add(off).readByteArray(n);
  return Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join(" ");
}
send("moves=" + rd(0x2a031b4, 8));
send("win=" + rd(0x2abb69c, 4));
