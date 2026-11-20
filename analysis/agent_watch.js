const m = Process.findModuleByName("libcandycrushsaga.so");
const SITE = m.base.add(0x2b41f84);
let armed = false;

Interceptor.attach(SITE, {
  onEnter() {
    if (armed) return;
    const self = this.context.x20;
    if (!self || self.isNull()) return;
    armed = true;
    send("SITE fired obj=" + self);
    try {
      const vt = self.readPointer();
      const fn = vt.add(0x118).readPointer();
      const f = new NativeFunction(fn, "int", ["pointer"]);
      send("moves now = " + f(self));
    } catch (e) {
      send("value err: " + e);
    }
    try {
      const base = self.and(ptr("0xfff").not());
      send("monitoring " + base);
      const writes = [];
      MemoryAccessMonitor.enable({ base, size: 0x8000 }, {
        onAccess(d) {
          if (writes.length > 300) return;
          const off = d.address.sub(self).toInt32();
          if (d.operation === "write" && off >= 0 && off < 0xa00) {
            let v = null;
            try { v = d.address.readS32(); } catch (e) {}
            writes.push(off.toString(16) + ":" + v);
          }
        },
      });
      setTimeout(() => {
        try { MemoryAccessMonitor.disable(); } catch (e) {}
        send("writes(" + writes.length + ") " + writes.join(" "));
      }, 6000);
    } catch (e) {
      send("monitor err: " + e);
    }
  },
});
