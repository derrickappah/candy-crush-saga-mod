const m = Process.findModuleByName("libcandycrushsaga.so");
let paidObj = null;
let freeObj = null;
let n = 0;

Interceptor.attach(m.base.add(0x3b15d54), {
  onEnter() {
    const o = this.context.x0;
    if (o.isNull()) return;
    paidObj = o;
    if (++n % 300 === 0) {
      try { o.add(0x14).writeS32(60000); } catch (e) {}
    }
  },
});

Interceptor.attach(m.base.add(0x3b15c38), {
  onEnter() {
    const o = this.context.x0;
    if (o.isNull()) return;
    freeObj = o;
    if (++n % 300 === 0) {
      try { o.add(0x18).writeS32(60000); } catch (e) {}
    }
  },
});

setInterval(() => {
  if (paidObj) { try { paidObj.add(0x14).writeS32(60000); } catch (e) {} }
  if (freeObj) { try { freeObj.add(0x18).writeS32(60000); } catch (e) {} }
}, 200);

send("ready");
