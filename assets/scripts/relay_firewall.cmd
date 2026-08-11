@echo off

netsh advfirewall firewall show rule name="relay5050in" >nul 2>&1

if errorlevel 1 (
    netsh advfirewall firewall add rule ^
    name="relay5050in" ^
    dir=in ^
    action=allow ^
    protocol=TCP ^
    localport=5050
)

netsh advfirewall firewall show rule name="relay5050out" >nul 2>&1

if errorlevel 1 (
    netsh advfirewall firewall add rule ^
    name="relay5050out" ^
    dir=out ^
    action=allow ^
    protocol=TCP ^
    localport=5050
)

exit