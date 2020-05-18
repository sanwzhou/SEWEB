cd /d %~dp0
%1 start "" mshta vbscript:createobject("shell.application").shellexecute("""%~0""","::",,"runas",1)(window.close)&amp;exit
reg add HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\0001 /v NetworkAddress /t REG_SZ /d 107B448F76B0 /f
ipconfig/renew "ÒÔÌ«Íø 2"
