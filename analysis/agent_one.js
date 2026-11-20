const m = Process.findModuleByName("libcandycrushsaga.so");
const off = parseInt(Process.argv ? "0" : "0") || 0;
const target = Number(Process.env && Process.env.X ? Process.env.X : 0);
