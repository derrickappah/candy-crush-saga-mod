const m = Process.findModuleByName("libcandycrushsaga.so");
function hex(off) {
  return Array.from(new Uint8Array(m.base.add(off).readByteArray(4)))
    .map((x) => ("0" + x.toString(16)).slice(-2)).join("");
}
send("moves(2a031b4)=" + hex(0x2a031b4) + " expect 600c8052");
send("boosters(22fb08c)=" + hex(0x22fb08c) + " expect 600c8052");
send("lives_tick(1ec9c80)=" + hex(0x1ec9c80) + " expect 2a0080d2");
send("dbgview(1f0fc54)=" + hex(0x1f0fc54) + " expect 1f2003d5");
send("testingmenu(1e81bf8)=" + hex(0x1e81bf8) + " expect 20008052");
