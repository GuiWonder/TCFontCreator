[简体中文](../../#中文字体简繁处理工具) **繁體中文** 
# 中文字型簡繁處理工具
繁體字型製作 簡轉繁字型 同義字(簡體字 繁體字 異體字)補全字型檔 合併簡繁字型 合併字型等。
## 功能
#### 1. 生成簡轉繁字型
提供繁體、繁體臺灣、繁體香港、繁體舊字形 4 種風格。
對於簡繁一對多情況可選擇不處理、使用單一常用字、使用詞彙正確處理簡繁一對多。
#### 2. 同義字補全字型檔
使用字型檔中存在的異體字、繁體字、簡體字補全缺失的字元，在不增加字形的情況下可顯示更多的字元。
#### 3. 合併簡繁字型
簡體與簡體編碼的簡入繁出字型合併。針對於簡體編碼的簡繁字型的合併。
#### 4. 合併兩個字型
可以是簡體 GB2312 併入繁體 BIG5 的字型，也可以是字元較少的字型併入字元較全的字型，用以補充字型檔中字形的數目。
#### 5. 日本字型新字形轉為舊字形
針對部分日本字型的處理。
#### 6. 生成繁轉簡字型
繁入簡出的字型。
#### 7. 生成簡轉繁字型臺灣詞彙
包含臺灣常用語以及化學元素名稱的轉換。

## 常見問題
#### 1. 如何在 Linux 或 Mac 上使用？
答：在終端中執行 `python run_in_command_line.py` 或 `python3 run_in_command_line.py`。*註:執行前需要先將 otfcc 相關檔案新增允許執行許可權`chmod +x ./otfcc/*`。*
#### 2. 某些字型處理失敗怎麼辦？
答：工具提供 oftcc 和 FontForge 兩種字型處理方法，如果處理失敗，可嘗試換另一種。
#### 3. 已經安裝過 FontForge 、Python 可否不使用程式附帶的 FontForge 、Python？
答：可以。需要在 **appdata** 檔案中指定 fontforge.exe、python.exe 所在的全路徑。
#### 4. 如何顯示轉換過程中的命令視窗？
答：主程式新增 `cmd` 引數可顯示轉換過程中的命令視窗。
#### 5. 對於轉換規則不滿意，可否自行修改？
答：可以。本工具轉換規則來自[OpenCC](https://github.com/BYVoid/OpenCC)，所使用的轉換字典為純文字格式，位於 **datas** 目錄中。
#### 6. 簡轉繁字型侷限性
答：使用詞彙的簡轉繁字型的侷限性可參閱[《正確實現簡轉繁字體》](https://ayaka.shn.hk/s2tfont/)，其他方法的簡轉繁字型見本帳戶其他字型專案。

## 下載地址
可從 [Releases](https://github.com/GuiWonder/TCFontCreator/releases) 頁面下載最新版。

## 特別感謝
* [otfcc](https://github.com/caryll/otfcc)
* [FontForge](https://github.com/fontforge/fontforge)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC)
* [《正確實現簡轉繁字型》](https://ayaka.shn.hk/s2tfont/hant/)、[繁媛明朝](https://github.com/ayaka14732/FanWunMing) 作者 [Ayaka](https://github.com/ayaka14732)

## 其他說明
本工具網址 https://github.com/GuiWonder/TCFontCreator
