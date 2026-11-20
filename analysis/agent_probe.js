const m = Process.findModuleByName("libcandycrushsaga.so");
const vt = m.base.add(0x4e57ab8);
send("base=" + m.base + " size=" + m.size);
send("vt raw: " + vt.readPointer() + " " + vt.add(8).readPointer() + " " + vt.add(16).readPointer());
send("slot77=" + vt.add(16 + 77 * 8).readPointer() + " expect=" + m.base.add(0x2a033e0));
send("slot8=" + vt.add(16 + 8 * 8).readPointer() + " expect=" + m.base.add(0x2a02f1c));
// who points at the getter anywhere in rw memory (function pointer tables)
const pat = Memory.alloc(8);
pat.writePointer(m.base.add(0x2a033e0));
