set ModuleName=chatmaya

REM The code snippet `%~dp0` is a special parameter expansion used in batch scripting to retrieve the drive letter and path of the current batch script file.
REM
REM Explanation:
REM - `%0` represents the current batch script file.
REM - `%~dp` is a combination of special characters that perform specific actions on the parameter.
REM - `%~d` extracts the drive letter of the specified parameter.
REM - `%~p` extracts the path of the specified parameter.
REM
REM Therefore, `%~dp0` combines these expansions to provide the drive letter and path of the current batch script file.
REM
REM Example:
REM If the batch script file is located at "C:\Scripts\example.bat", `%~dp0` will output "C:\Scripts\".
set CurrentPath=%~dp0

REM The code snippet `%CurrentPath:~0,-2%` is a substring extraction operation used in batch scripting to manipulate the value of the variable `CurrentPath`.
REM
REM Explanation:
REM - `%CurrentPath%` represents the variable containing a path or string.
REM - `:~0,-2` is a substring extraction syntax that specifies which part of the variable to extract.
REM
REM Breakdown of `:~0,-2`:
REM - `:~` indicates that a substring operation is being performed.
REM - `0` specifies the starting index of the substring. In this case, it starts from the beginning of the string (index 0).
REM - `-2` specifies the length of the substring to extract. The negative sign indicates counting from the end of the string, and `-2` means to exclude the last two characters.
REM
REM Functionality:
REM - `%CurrentPath:~0,-2%` will extract a substring from `CurrentPath` starting from the beginning and excluding the last two characters.
REM
REM Example:
REM If `CurrentPath` contains the value "C:\Folder\Subfolder\", `%CurrentPath:~0,-2%` will output "C:\Folder\Subfolder" by excluding the last two characters, which are the backslash and the character before it.
set A=%CurrentPath:~0,-2%

REM This script extracts the drive and path of the items in variable %A
REM and stores it in the variable RootPath
for %%A in (%A%) do (
    REM For each item in %A, iterate and set RootPath to the drive and path
    set RootPath=%%~dpA
)

set MayaPy="%ProgramFiles%\Autodesk\Maya%MayaVersion%\bin\mayapy.exe"

:: pip upgrade
%MayaPy% -m pip install -U pip

:: install site-packages
%MayaPy% -m pip install -U -r %CurrentPath%\requirements.txt -t %UserProfile%\Documents\maya\%MayaVersion%\scripts\site-packages

:: install module
robocopy %RootPath%\scripts\%ModuleName% %UserProfile%\Documents\maya\%MayaVersion%\scripts\%ModuleName% /MIR