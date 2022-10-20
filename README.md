**简体中文** [繁體中文](README-TC.md#中文字型簡繁處理工具) 
# 中文字体简繁处理工具
繁体字体制作 简转繁字体 同义字(简体字 繁体字 异体字)补全字库 合并简繁字体 合并字体等。

## 功能
#### 1. 生成繁体字体
提供繁体、繁体台湾、繁体香港、繁体旧字形 4 种风格。
对于简繁一对多情况可选择不处理、使用单一常用字、使用词汇正确处理简繁一对多。
#### 2. 同义字补全字库
使用字库中存在的异体字、繁体字、简体字补全缺失的字符，在不增加字形的情况下可显示更多的字符。
#### 3. 合并简繁字体
简体 GB2312 与繁体 GB2312 字体合并。针对于简体中文 GB2312 编码的简繁字体的合并。
#### 4. 合并两个字体
可以是简体 GB2312 并入繁体 BIG5 的字体，也可以是字符较少的字体并入字符较全的字体，用以补充字库中字形的数目。
#### 5. 日本新字转为传承正字
针对日本字体的处理。

## 常见问题
#### 1. 如何显示转换过程中的命令窗口？
答：主程序添加 `cmd` 参数可显示转换过程中的命令窗口。
#### 2. 如何在 Linux 或 Mac 上使用？
答：在终端中运行 `python run_in_command_line.py` 或 `python3 run_in_command_line.py`。*注:运行前需要先将 otfcc 相关文件添加允许执行权限`chmod +x ./otfcc/*`。*
#### 3. 已经安装过 FontForge 、Python 可否不使用程序附带的 FontForge 、Python？
答：可以。需要在 **appdata** 文件中指定 fontforge.exe、python.exe 所在的全路径。
#### 4. 为什么执行同义字补全或合并字体后仍会有一些字形显示为空白？
答：某些字体本身就含有一些带有码位的空白字形，处理这种字体时应该先使用字体编辑软件将这些字形删除。例如可以使用 FontCreator 打开字体，找到“未完成的字符（Incomplete Characters）”，并将他们删除。
#### 5. 某些字体处理失败怎么办？
答：工具提供 oftcc 和 FontForge 两种字体处理方法，如果处理失败，可尝试换另一种。如果都失败（较为罕见）可以试一下其他字体处理软件是否能够读取字体，如果可以正确读取，将字体重新生成一次，一般都可解决此问题。
#### 6. 对于转换规则不满意，可否自行修改？
答：可以。所有转换字典均为纯文本格式，位于 **datas** 目录中。

## 下载地址
可从 [Releases](https://github.com/GuiWonder/TCFontCreator/releases) 页面下载最新版。

## 特别感谢
* [otfcc](https://github.com/caryll/otfcc)
* [FontForge](https://github.com/fontforge/fontforge)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC)
* [《正确实现简转繁字体》](https://ayaka.shn.hk/s2tfont/)
