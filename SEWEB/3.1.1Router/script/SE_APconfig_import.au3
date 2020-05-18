;ControlFocus("title","text",controlID)Edit1=Edit instance 1
ControlFocus("打开","","Edit1")
;Wait10secondsfortheUploadwindowtoappear
WinWait("[CLASS:#32770]","",10)
;Set the File name text on the Edit field
ControlSetText("打开","","Edit1","D:\python\SEWEB\3.1.1Router\tmp\apUpdateConf3333.tar.gz")
Sleep(2000)
;Click on the Open button
ControlClick("打开","","Button1");