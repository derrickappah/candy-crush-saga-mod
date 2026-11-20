const m = Process.findModuleByName("libcandycrushsaga.so");
const SITE = m.base.add(0x2b41f84);
let done = false;
let last = -1;

Interceptor.attach(SITE, {
  onEnter() {
    if (done) return;
    const self = this.context.x20;
    if (!self || self.isNull()) return;
    done = true;
    const vt = self.readPointer();
    const fn = vt.add(0x118).readPointer();
    send("vm=" + self + " vt=" + vt + " fn=" + fn);

    // dump object
    send("obj: " + hexdump(self, { length: 0x80, ansi: false }));

    Interceptor.attach(fn, {
      onEnter() { this.s = this.context.x0; },
      onLeave(ret) {
        const v = ret.toInt32();
        if (v !== last) {
          last = v;
          send("ret=" + v + " this=" + this.s);
          if (v < 40 && v >= 0) {
            send("bt: " + Thread.backtrace(this.context, Backtracer.FUZZY).slice(0, 6).map(a => a.sub(m.base)).join(" "));
            send("this obj: " + hexdump(this.s, { length: 0x60, ansi: false }));
          }
        }
      },
    });
    send("hooked");
  },
});
