const m = Process.findModuleByName("libcandycrushsaga.so");
let done = false;
let count = 0;

function paint(obj) {
  try {
    obj.add(0x14).writeS32(60000);
    obj.add(0x18).writeS32(60000);
  } catch (e) {}
}

for (const off of [0x3b15d54, 0x3b15c38]) {
  Interceptor.attach(m.base.add(off), {
    onEnter() {
      if (!done) {
        done = true;
        send("object " + this.context.x0);
      }
      const obj = this.context.x0;
      if (obj.isNull()) return;
      if (++count % 500 === 0) paint(obj);
    },
  });
}
send("ready");
