@echo off
if not "%1"=="am_admin" (
  powershell start -verb runas '%0' am_admin
  y:
  cd "Y:\games\Grand Theft Auto V"
  start "" "Y:\games\Grand Theft Auto V\GTAVLauncher.exe"
) else (
  rmdir "C:\ProgramData\Steam"
  mklink /D "C:\ProgramData\Steam" "C:\ProgramData\Steam-dave"
  rmdir "C:\ProgramData\Socialclub"
  mklink /D "C:\ProgramData\Socialclub" "C:\ProgramData\Socialclub-dave"
)