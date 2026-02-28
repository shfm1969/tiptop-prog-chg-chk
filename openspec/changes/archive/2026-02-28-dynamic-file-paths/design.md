## Context

目前專案的兩個主要處理檔案：`input_data` 與 `output_data`，在腳本 `chklog.py` 內皆以絕對路徑寫死（例如 `d:\AI_Study\...`）。這意味著當專案放置於不同的目錄或由不同的開發者操作時，必須手動修改程式碼中的路徑常數才能執行，這會降低開發與使用的便利性。

## Goals / Non-Goals

**Goals:**
- 將腳本內的路徑常數改為使用專案目錄為基準點的相對計算方式。
- 專案根目錄必須能透過程式的所在位置（通常是 `__file__`）去自動推導。
- 無論使用者在哪個目錄執行 `uv run python chklog.py`，程式都能讀寫到正確的 `input_data/` 來源與 `output_data/` 目標。

**Non-Goals:**
- 不會去從外部動態傳入命令列參數 (CLI arguments) 指定路徑（為保持與現有用法的相容性與簡潔性，暫不加入 `argparse`）。
- 不會變更 Excel 或 TXT 檔案的解析邏輯與核心比對邏輯。

## Decisions

- **使用 `os.path.abspath` 與 `os.path.dirname` 來定位**：
  在 `chklog.py` 中，使用 `BASE_DIR = os.path.dirname(os.path.abspath(__file__))` 來獲取當前腳本所在的目錄（即專案根目錄）。
- **使用 `os.path.join` 來組合路徑**：
  原有的 `EXCEL_PATH`、`TXT_4GL_4FD`、`TXT_RPT_XML` 與 `OUTPUT_DIR` 常數，將改為透過 `os.path.join(BASE_DIR, 'input_data', '...')` 的方式動態產生。這能確保在不同作業系統（Windows / Linux / macOS）下路徑分隔符號的相容性。

## Risks / Trade-offs

- [Risk] 如果使用者將 `chklog.py` 移動到專案根目錄以外的地方執行 ??Mitigation 目前腳本與資料夾的相對位置是固定的，只要不破壞專案結構就不會有問題。這也是大部分 Python 專案的慣用做法。
