const m = Process.findModuleByName("libcandycrushsaga.so");
const FN = m.base.add(0x22fafd0);
let n = 0;
const orig = new NativeFunction(FN, "int", ["pointer", "int"]);

Interceptor.attach(FN, {
  onEnter() {
    if (n++ > 12) return;
    this.id = this.context.x1.toInt32 ? this.context.x1.toInt32() : this.context.w1;
    send("GetAmount id=" + this.context.w1);
  },
  onLeave(ret) {
    if (n > 13) return;
    send("  -> " + ret.toInt32());
  },
});
send("ready");
