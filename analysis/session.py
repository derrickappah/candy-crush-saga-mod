import subprocess, sys, time, frida

ADB = r"C:\Users\DELL\AppData\Local\Android\Sdk\platform-tools\adb.exe"
AGENT = sys.argv[1]
SWIPES = int(sys.argv[2]) if len(sys.argv) > 2 else 10
PAUSE = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0

pid = int(subprocess.check_output([ADB, "shell", "pidof", "com.king.candycrushsaga"]).split()[0])
print("pid", pid, flush=True)

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
session = dev.attach(pid)
print("attached", flush=True)

msgs = []
script = session.create_script(open(AGENT, encoding="utf-8").read())
def on_msg(m, d):
    msgs.append(str(m.get("payload")))
    print("MSG", m.get("payload"), flush=True)
    if m.get("type") == "error":
        print("ERR", m.get("description"), "\n", m.get("stack"), flush=True)

script.on("message", on_msg)
script.load()
print("loaded", flush=True)

time.sleep(6)
for i in range(SWIPES):
    subprocess.run([ADB, "shell", "input", "swipe", "540", "1140", "660", "1140", "320"])
    time.sleep(PAUSE)
print("done, msgs:", len(msgs), flush=True)
