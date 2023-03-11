REM 该脚本可以实现让用户选择一种日期设置方式，然后使用管理员权限设置新日期。
@echo off
chcp 65001

echo 日期设置方式（输入 1、2 或 3）： && echo 1. 设置为默认日期，例如 2011 年 3 月 11 日 && echo 2. 输入新日期（格式为 yyyy/mm/dd） && echo 3. 设置为当前日期


:input_option
REM 提示用户选择日期设置方式
set /p OPTION=请选择日期设置方式（输入 1、2 或 3）:
IF /I "%OPTION%"=="1" (
REM 设置为默认日期，例如 2011 年 3 月 11 日
set NEW_DATE=2011/3/11
) ELSE IF /I "%OPTION%"=="2" (
REM 提示用户输入要更改的日期
set /p NEW_DATE=请输入新日期（格式为 yyyy/mm/dd）:
) ELSE IF /I "%OPTION%"=="3" (
REM 设置为当前日期
set NEW_DATE=2023/3/11
) ELSE (
echo 无效的选项，请输入 1、2 或 3.
goto input_option
)

REM 使用管理员权限设置新日期
powershell.exe -Command "Start-Process cmd -Verb runAs -ArgumentList '/c date %NEW_DATE%'"

REM 确认日期已更改
echo 日期已更改为 %NEW_DATE%.

REM 等待用户按下任意键后退出
pause