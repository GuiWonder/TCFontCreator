@echo off

echo 开始编译
"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv" /build "Release|x64" TCFontCreator.sln
echo 编译完成
pause
