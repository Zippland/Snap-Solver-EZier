Set oShell = CreateObject("WScript.Shell")
Set oFSO = CreateObject("Scripting.FileSystemObject")

' 获取当前脚本所在目录
strCurrentPath = oFSO.GetParentFolderName(WScript.ScriptFullName)

' 构建 init.py 的完整路径
strInitPath = strCurrentPath & "\init.py"

' 使用 pythonw.exe 无窗口运行 init.py
cmd = "cmd /c start /b pythonw """ & strInitPath & """"
oShell.Run cmd, 0, False