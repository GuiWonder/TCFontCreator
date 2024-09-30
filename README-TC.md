[简体中文](../../#中文字体简繁处理工具) **繁體中文** 

# 中文字型簡繁處理工具
簡繁轉換字型製作 同義字(簡體字 繁體字 異體字)補全字型檔 合併簡繁字型 合併字型。

## 功能
### 生成簡繁轉換字型
#### 1. 生成簡轉繁字型
可選擇繁體預設、繁體臺灣、繁體香港、繁體舊字形 4 種繁體異體字。
對於簡繁一對多情況可選擇不處理一簡多繁、使用單一常用字、使用詞彙動態匹配一簡多繁、使用臺灣詞彙動態匹配（包含臺灣常用語以及化學元素名稱的轉換）。
#### 2. 生成繁轉簡字型
繁入簡出的字型。
### 補充字型檔
#### 1. 從其他字型檔補入
可一次補入多個字型檔。
#### 2. 使用字型本身簡繁異體補充
使用字型檔中存在的異體字、繁體字、簡體字補全缺失的字元，在不增加字形的情況下可顯示更多的字元。
#### 3. 合併簡體與簡入繁出字型
針對於簡體編碼的簡繁字型的合併。
### 操作介面
#### 1. Windows 系統
Windows 系統下可直接使用圖形介面。
#### 2. Linux 或 Mac 系統
需在終端中執行，在終端中執行 `python run_in_command_line_tc.py` 或 `python3 run_in_command_line_tc.py`。執行前需要確保 otfcc 相關檔案已新增允許執行許可權，`chmod +x ./otfcc/*`。

## 常見問題
#### 1. 某些字型處理失敗怎麼辦？
答：工具提供 oftcc 和 FontForge 兩種字型處理方法，如果處理失敗，可嘗試換另一種。
#### 2. 圖形介面下如何顯示轉換過程中的命令視窗？
答：主程式新增 `cmd` 引數可顯示轉換過程中的命令視窗。
#### 3. 對於轉換規則不滿意，可否自行修改？
答：可以。本工具轉換規則來自[OpenCC](https://github.com/BYVoid/OpenCC)，所使用的轉換字典為純文字格式，位於 **datas** 目錄中。
#### 4. 簡轉繁字型注意問題及侷限性
答：使用詞彙的簡轉繁字型需要使用 OpenType 功能。侷限性可參閱[《正確實現簡轉繁字型》](https://ayaka.shn.hk/s2tfont/hant/)，其他方法的簡轉繁字型見本帳戶其他字型專案。

## 下載地址
可從 [Releases](https://github.com/GuiWonder/TCFontCreator/releases) 頁面下載。

## 特別感謝
* [otfcc](https://github.com/caryll/otfcc)
* [FontForge](https://github.com/fontforge/fontforge)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC)
* [《正確實現簡轉繁字型》](https://ayaka.shn.hk/s2tfont/hant/)、[繁媛明朝](https://github.com/ayaka14732/FanWunMing)

