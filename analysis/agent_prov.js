const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
Interceptor.attach(m.base.add(0x1d9a368), {
  onEnter() {
    if (n++ > 4) return;
    let p = ptr(0), off = "?";
    try { p = this.context.x0.add(0x10).readPointer(); off = p.sub(m.base); } catch (e) {}
    send("provider=" + off + " id=" + this.context.w1 + " self=" + this.context.x0);
  },
});
send("ready");
