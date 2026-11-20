const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;

function hook(addr, tag) {
  Interceptor.attach(m.base.add(addr), {
    onEnter() {
      if (n++ > 25) return;
      this.t = tag;
      send(tag + " enter id=" + this.context.w1 + " self=" + this.context.x0);
    },
    onLeave(ret) {
      if (n > 27) return;
      send(tag + " leave ret=" + ret);
    },
  });
}
hook(0x22faeec, "s2");
hook(0x22fafd0, "s3");
hook(0x22fb0f8, "s4");
send("ready");
