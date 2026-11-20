const m = Process.findModuleByName("libcandycrushsaga.so");
const SITE = m.base.add(0x2b41f84);
let n = 0;

function dwords(p, count) {
  const out = [];
  for (let i = 0; i < count; i++) {
    try { out.push(p.add(i * 4).readS32()); } catch (e) { out.push(null); }
  }
  return out.join(",");
}

Interceptor.attach(SITE, {
  onEnter() {
    if (n > 30) return;
    n++;
    const self = this.context.x20;
    if (!self || self.isNull()) return;
    const vt = self.readPointer();
    const fn = vt.add(0x118).readPointer();
    let v = -1;
    try { v = new NativeFunction(fn, "int", ["pointer"])(self); } catch (e) {}
    send("v=" + v + " disc=" + self.add(0x190).readS32() +
      " 100:" + dwords(self.add(0x100), 8) +
      " 180:" + dwords(self.add(0x180), 8) +
      " 9a8=" + self.add(0x9a8).readS32());
  },
});
send("ready");
