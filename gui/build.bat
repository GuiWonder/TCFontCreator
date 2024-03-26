@echo off

echo Begin
msbuild TCFontCreator.sln /p:Configuration=Release /p:Platform=x64
echo Finnished
pause
