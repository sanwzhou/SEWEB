cd /d %~dp0
%1 start "" mshta vbscript:createobject("shell.application").shellexecute("""%~0""","::",,"runas",1)(window.close)&amp;exit
netsh interface ip set address name="��̫�� 2" source=static addr=192.168.198.39 mask=255.255.255.0 gateway=192.168.198.1 1
netsh interface ip set dns name="��̫�� 2" source=static addr=223.5.5.5