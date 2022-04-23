# 中文字体简繁处理工具
可轻而易举地完成繁体字体制作、同义字补全字库、合并简繁字体等。

## 功能
#### 1. 生成繁体字体
提供繁体、繁体TW、繁体HK、繁体旧字形 4 种风格。
对于简繁一对多情况可选择不处理、使用单一常用字、使用词汇正确处理简繁一对多。
#### 2. 同义字补全字库
使用字库中存在的异体字、繁体字、简体字补全缺失的字符，在不增加字形的情况下可显示更多的字符。
#### 3. 日本新字转为传承正字
针对日本字体的处理。
#### 4. 合并简繁字体
简体 GB2312 与繁体 GB2312 字体合并。针对于简体中文 GB2312 编码的简繁字体的合并。
#### 5. 合并两个字体
可以是简体 GB2312 与繁体 BIG5 的字体，也可以是字形较少的字体与字形较全的字体，用以补充字库中字形的数目。

## 常见问题
#### 1. 如何显示转换过程中的命令窗口？
答：主程序添加 `cmd` 参数可显示转换过程中的命令窗口。
#### 2. 已经安装过 FontForge 、Python 可否不使用程序附带的 FontForge 、Python？
答：可以。需要在 **appdata** 文件中指定 fontforge.exe、python.exe 所在的全路径。
#### 3. 如何在 Linux 或 Mac 上使用？
答：在终端中运行 `python run_in_command_line.py` 或 `python3 run_in_command_line.py`。运行前需要先将 otfcc 相关文件添加允许执行权限`chmod +x ./otfcc/*`。
#### 4. 为什么执行同义字补全或合并字体后仍会有一些字形显示为空白？
答：某些字体本身就含有一些带有码位的空白字形，处理这种字体时应该先使用字体编辑软件将这些字形删除。例如可以使用 FontCreator 打开字体，找到“未完成的字符（Incomplete Characters）”，并将他们删除。
#### 5. 某些字体无法读取怎么办？
答：可以试一下其他字体处理软件是否能够读取字体，如果可以正确读取，将字体重新生成一次，一般都可解决此问题。
#### 6. 对于转换规则不满意，可否自行修改？
答：可以。所有转换字典均为纯文本格式，位于 **datas** 目录中。

## 下载地址
可从 [Releases](https://github.com/GuiWonder/TCFontCreator/releases) 页面下载最新版。

## 本项目中引用的项目
* [otfcc](https://github.com/caryll/otfcc)
* [FontForge](https://github.com/fontforge/fontforge)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC)


# 中文字型簡繁處理工具
可輕而易舉地完成繁體字體制作、同義字補全字型檔、合併簡繁字型等。

## 功能
#### 1. 生成繁體字型
提供繁體、繁體TW、繁體HK、繁體舊字形 4 種風格。
對於簡繁一對多情況可選擇不處理、使用單一常用字、使用詞彙正確處理簡繁一對多。
#### 2. 同義字補全字型檔
使用字型檔中存在的異體字、繁體字、簡體字補全缺失的字元，在不增加字形的情況下可顯示更多的字元。
#### 3. 日本新字轉為傳承正字
針對日本字型的處理。
#### 4. 合併簡繁字型
簡體 GB2312 與繁體 GB2312 字型合併。針對於簡體中文 GB2312 編碼的簡繁字型的合併。
#### 5. 合併兩個字型
可以是簡體 GB2312 與繁體 BIG5 的字型，也可以是字形較少的字型與字形較全的字型，用以補充字型檔中字形的數目。

## 常見問題
#### 1. 如何顯示轉換過程中的命令視窗？
答：主程式新增 `cmd` 引數可顯示轉換過程中的命令視窗。
#### 2. 已經安裝過 FontForge 、Python 可否不使用程式附帶的 FontForge 、Python？
答：可以。需要在 **appdata** 檔案中指定 fontforge.exe、python.exe 所在的全路徑。
#### 3. 如何在 Linux 或 Mac 上使用？
答：在終端中執行 `python run_in_command_line.py` 或 `python3 run_in_command_line.py`。執行前需要先將 otfcc 相關檔案新增允許執行許可權`chmod +x ./otfcc/*`。
#### 4. 為什麼執行同義字補全或合併字型後仍會有一些字形顯示為空白？
答：某些字型本身就含有一些帶有碼位的空白字形，處理這種字型時應該先使用字型編輯軟體將這些字形刪除。例如可以使用 FontCreator 開啟字型，找到“未完成的字元（Incomplete Characters）”，並將他們刪除。
#### 5. 某些字型無法讀取怎麼辦？
答：可以試一下其他字型處理軟體是否能夠讀取字型，如果可以正確讀取，將字型重新生成一次，一般都可解決此問題。
#### 6. 對於轉換規則不滿意，可否自行修改？
答：可以。所有轉換字典均為純文字格式，位於 **datas** 目錄中。

## 下載地址
可從 [Releases](https://github.com/GuiWonder/TCFontCreator/releases) 頁面下載最新版。

## 本專案中引用的專案
* [otfcc](https://github.com/caryll/otfcc)
* [FontForge](https://github.com/fontforge/fontforge)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC)
