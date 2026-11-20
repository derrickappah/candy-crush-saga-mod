const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
const A = [0x1f26178, 0x1f2617c, 0x1f26074, 0x1f260d0, 0x1f260e0];
A.forEach((a, i) => {
  try {
    Interceptor.attach(m.base.add(a), {
      onEnter() {
        if (n++ > 20) return;
        send("slot" + i + " x0=" + this.context.x0 + " x1=" + this.context.x1 +
             " w2=" + this.context.x2.toUInt32());
      },
    });
  } catch (e) {}
});
send("ready");
