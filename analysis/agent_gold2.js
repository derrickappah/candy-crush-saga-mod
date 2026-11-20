const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
Interceptor.attach(m.base.add(0x20f553c), {
  onEnter() {
    if (n++ > 6) return;
    send("SetFreeBalance(" + this.context.x1.toUInt32() + ") on " + this.context.x0);
  },
});
Interceptor.attach(m.base.add(0x20f58a8), {
  onEnter() {
    if (n++ > 6) return;
    send("PublishBalances on " + this.context.x0 +
         " +0x14=" + this.context.x0.add(0x14).readS32() +
         " +0x18=" + this.context.x0.add(0x18).readS32());
  },
});
send("ready");
