;ControlFocus("title","text",controlID)Edit1=Edit instance 1
ControlFocus("��","","Edit1")
;Wait10secondsfortheUploadwindowtoappear
WinWait("[CLASS:#32770]","",10)
;Set the File name text on the Edit field
ControlSetText("��","","Edit1","D:\python\SEWEB\3.1.1Router\script\WA3000Nv2.6.2-160107.bin")
Sleep(2000)
;Click on the Open button
ControlClick("��","","Button1");