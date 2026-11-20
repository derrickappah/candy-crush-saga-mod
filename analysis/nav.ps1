$adb = "C:\Users\DELL\AppData\Local\Android\Sdk\platform-tools\adb.exe"
$py = "C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe"
Set-Location "C:\Users\DELL\Downloads\candy crach 2\work"
function Shot($n) { & $adb shell screencap -p "/sdcard/$n.png" | Out-Null; & $adb pull "/sdcard/$n.png" "$n.png" 2>&1 | Out-Null; return (& $py ocr.py "$n.png" 2>&1) }
function TapC($line) { if ($line -match 'x=(\d+)-(\d+) y=(\d+)-(\d+)') { & $adb shell input tap ([int](([int]$Matches[1] + [int]$Matches[2]) / 2)) ([int](([int]$Matches[3] + [int]$Matches[4]) / 2)) } }

for ($i = 0; $i -lt 6; $i++) {
  & $adb shell input keyevent 4
  Start-Sleep -Seconds 3
  $o = Shot "n$i"
  $q = $o | Select-String -Pattern "Quit level"
  if ($q) {
    $line = $o | Select-String -Pattern "Quit$"
    TapC $line
    Start-Sleep -Seconds 10
    & $adb shell input keyevent 4
    Start-Sleep -Seconds 3
    break
  }
}
$o = Shot "now"
$o | Select-Object -First 10
