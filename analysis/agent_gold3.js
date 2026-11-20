const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
function h(off, tag) {
  Interceptor.attach(m.base.add(off), {
    onEnter() {
      if (n++ > 8) return;
      send(tag + " x0=" + this.context.x0 + " w1=" + this.context.x1.toUInt32() +
           " w2=" + this.context.x2.toUInt32());
    },
  });
}
h(0x20f5268, "SetBalances");
h(0x20f58a8, "Publish");
h(0x20f553c, "SetFree");
send("ready");
