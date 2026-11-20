import subprocess, sys, time, frida

ADB = r"C:\Users\DELL\AppData\Local\Android\Sdk\platform-tools\adb.exe"
PKG = "com.king.candycrushsaga"
ACT = "com.king.candycrushsaga.CandyCrushSagaActivity"
AGENT = sys.argv[1]
SWIPES = int(sys.argv[2]) if len(sys.argv) > 2 else 10
PAUSE = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0


def sh(*a):
    return subprocess.run([ADB, "shell", *a], capture_output=True).stdout.decode(errors="replace").strip()


def wait_pid(timeout=60):
    end = time.time() + timeout
    while time.time() < end:
        out = sh("pidof", PKG)
        if out:
            return int(out.split()[0])
        time.sleep(1)
    raise SystemExit("no pid")


sh("am", "force-stop", PKG)
time.sleep(2)
sh("am", "start", "-n", f"{PKG}/{ACT}")
pid = wait_pid()
print("pid", pid, flush=True)
time.sleep(15)
subprocess.run([ADB, "forward", "--remove-all"], capture_output=True)
subprocess.run([ADB, "forward", "tcp:27042", "tcp:27042"], capture_output=True)
time.sleep(1)

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
for attempt in range(6):
    try:
        session = dev.attach(pid)
        break
    except Exception as e:
        print("attach retry", attempt, e, flush=True)
        time.sleep(2)
else:
    raise SystemExit("attach failed")

print("attached", flush=True)
msgs = []
script = session.create_script(open(AGENT, encoding="utf-8").read())
script.on("message", lambda m, d: (msgs.append(str(m.get("payload"))), print("MSG", m.get("payload"), flush=True)))
script.load()
print("loaded", flush=True)

time.sleep(8)
for i in range(SWIPES):
    sh("input", "swipe", "540", "1140", "660", "1140", "320")
    time.sleep(PAUSE)
print("done msgs", len(msgs), flush=True)
