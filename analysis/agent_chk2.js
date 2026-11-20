const m = Process.findModuleByName("libcandycrushsaga.so");
for (const off of [0x20f5a28, 0x20f5a30]) {
  const p = m.base.add(off);
  send(off.toString(16) + " " + Instruction.parse(p).toString());
}
send("done");
