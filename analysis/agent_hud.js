const m = Process.findModuleByName("libcandycrushsaga.so");
const SITE = m.base.add(0x2b41f84);   // start of the "movesLeft" binding block
let hooked = false;
let vmObj = null;

send("site=" + SITE);

Interceptor.attach(SITE, {
  onEnter() {
    const self = this.context.x20;
    if (!self || self.isNull()) return;
    let vt;
    try { vt = self.readPointer(); } catch (e) { return; }
    const fn = vt.add(0x118).readPointer();
    if (hooked) return;
    hooked = true;
    send("vm=" + self + " vtable=" + vt + " getter=" + fn);
    Interceptor.attach(fn, {
      onEnter() { this.self = this.context.x0; },
      onLeave(ret) {
        const v = ret.toInt32();
        send("movesLeft=" + v + " self=" + this.self);
        const base = this.self;
        const hits = [];
        for (let off = 0; off < 0x400; off += 4) {
          try { if (base.add(off).readS32() === v) hits.push(off.toString(16)); } catch (e) {}
        }
        send("  value also at offsets: " + hits.join(","));
      },
    });
    send("getter hooked");
  },
});
