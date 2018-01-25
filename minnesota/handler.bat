@Echo off
:Start

echo Program terminated at %Date% %Time% with Error %ErrorLevel% >> c:\logs\program.log 
echo Press Ctrl-C if you don't want to restart automatically
echo programs
cd %~dp0
start %1agent.exe

goto Start