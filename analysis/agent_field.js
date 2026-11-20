const m = Process.findModuleByName("libcandycrushsaga.so");
const SITE = m.base.add(0x2b41f84);
let n = 0;

Interceptor.attach(SITE, {
  onEnter() {
    if (n > 12) return;
    n++;
    const self = this.context.x20;
    if (!self || self.isNull()) return;
    const vt = self.readPointer();
    const fn = vt.add(0x118).readPointer();
    let v = -1;
    try { v = new NativeFunction(fn, "int", ["pointer"])(self); } catch (e) {}
    send("ret=" + v +
      " disc190=" + self.add(0x190).readS32() +
      " at100=" + self.add(0x100).readS32() +
      " at108=" + self.add(0x108).readS32() +
      " at110=" + self.add(0x110).readS32() +
      " at180=" + self.add(0x180).readS32() +
      " at188=" + self.add(0x188).readS32());
    if (n === 6) {
      send("dump100: " + hexdump(self.add(0x100), { length: 0x40, ansi: false }));
      send("dump180: " + hexdump(self.add(0x180), { length: 0x40, ansi: false }));
    }
  },
});
send("ready");
