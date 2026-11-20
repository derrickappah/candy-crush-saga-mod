$adb = "C:\Users\DELL\AppData\Local\Android\Sdk\platform-tools\adb.exe"
$py = "C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe"
Set-Location "C:\Users\DELL\Downloads\candy crach 2\work"

function Shot($name) {
  & $adb shell screencap -p "/sdcard/$name.png" | Out-Null
  & $adb pull "/sdcard/$name.png" "$name.png" 2>&1 | Out-Null
  return (& $py ocr.py "$name.png" 2>&1)
}
function TapCenter($line) {
  if ($line -match 'x=(\d+)-(\d+) y=(\d+)-(\d+)') {
    $x = ([int]$Matches[1] + [int]$Matches[2]) / 2
    $y = ([int]$Matches[3] + [int]$Matches[4]) / 2
    & $adb shell input tap ([int]$x) ([int]$y)
    Write-Host "tap $x,$y"
  }
}

# get to map
for ($i = 0; $i -lt 5; $i++) {
  & $adb shell input keyevent 4
  Start-Sleep -Seconds 3
  $o = Shot "g$i"
  $q = $o | Select-String -Pattern "Quit level"
  if ($q) { $quit = $o | Select-String -Pattern "^\S+\s+x=\S+ y=\S+\s+Quit$"; TapCenter $quit; Start-Sleep -Seconds 10; & $adb shell input keyevent 4; Start-Sleep -Seconds 4; break }
}

$o = Shot "map"
$o | Select-String -Pattern "Play|Map" | Select-Object -First 4
