@echo off

REM The code `set MayaVersion=2024` is a batch script command used to create or update a variable named `MayaVersion` with the value `2024`.

REM Explanation:
REM - `set`: This keyword is used in batch scripting to assign a value to a variable.
REM - `MayaVersion`: This is the name of the variable being created or updated.
REM - `2024`: This is the value assigned to the variable `MayaVersion`.

REM Functionality:
REM - When this code is executed in a batch script, it creates a variable named `MayaVersion` if it does not already exist, and assigns the value `2024` to it.
REM - If the `MayaVersion` variable already exists, running this command will update its value to `2024`.

REM Example:
REM If you run this code in a batch script, the variable `MayaVersion` will be created or updated with the value `2024`. Subsequently, you can reference this variable throughout the script to access or modify the Maya version number.
set MayaVersion=2024

call %~dp0install_win.bat

pause