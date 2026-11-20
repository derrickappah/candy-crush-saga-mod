const m = Process.findModuleByName("libcandycrushsaga.so");
for (const off of [0x3b15c38, 0x2e85924, 0x48067c0, 0x3b15d54]) {
  const p = m.base.add(off);
  const b = Array.from(new Uint8Array(p.readByteArray(8)));
  send(off.toString(16) + " now " + b.map((x) => x.toString(16).padStart(2, "0")).join(" ") +
       " | insn " + Instruction.parse(p).toString());
}
send("done");
