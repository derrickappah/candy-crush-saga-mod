const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
Interceptor.attach(m.base.add(0x1d9a368), {
  onEnter() {
    if (n++ > 3) return;
    let o = ptr(0), vt = ptr(0), t = ptr(0);
    try { o = this.context.x0.add(8).readPointer(); } catch (e) {}
    try { vt = o.readPointer(); } catch (e) {}
    try { t = vt.add(0xd0).readPointer(); } catch (e) {}
    send("obj=" + o + " vtOff=" + (vt.isNull() ? "?" : vt.sub(m.base)) +
         " slotD0=" + (t.isNull() ? "?" : t.sub(m.base)) + " id=" + this.context.w1);
  },
});
send("ready");
