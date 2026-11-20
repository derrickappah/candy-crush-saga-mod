const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
Interceptor.attach(m.base.add(0x21ddd28), {
  onEnter() {
    if (n++ > 6) return;
    const self = this.context.x0;
    const btn = this.context.x1;
    let svc = ptr(0), vptr = ptr(0);
    try { svc = self.add(0x28).readPointer(); } catch (e) {}
    try { if (!svc.isNull()) vptr = svc.readPointer(); } catch (e) {}
    let slots = "";
    try {
      for (const k of [0, 1, 2, 3]) {
        const t = vptr.add(k * 8).readPointer();
        slots += " s" + k + "=" + (t.isNull() ? "0" : t.sub(m.base));
      }
    } catch (e) {}
    send("click id=" + (btn.isNull() ? "?" : btn.add(0x28).readS32()) + slots);
  },
});
send("ready");
