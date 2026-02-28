## Why

目前 `chklog.py` 腳本中的輸入與輸出檔案路徑是「寫死 (hardcoded)」的絕對路徑。只要專案移動到其他開發者的電腦或是不同的目錄，腳本就會因為找不到路徑而執行失敗。為了解決這個缺乏可攜性 (portability) 的問題，我們需要讓腳本能夠自動以「專案根目錄」為基準點，動態尋找 `input_data` 與 `output_data` 資料夾。

## What Changes

- 修改 `chklog.py` 內定義檔案路徑的方式。
- 移除寫死的絕對路徑 (如 `d:\AI_Study\...`)。
- 使用 `os` 模組動態取得目前腳本所在的目錄，並以此組合出相對應的 `input_data/` 來源檔案路徑，以及 `output_data/` 輸出路徑。

## Capabilities

### New Capabilities
- `dynamic-file-paths`: 腳本能動態解析專案根目錄，不再依賴絕對路徑。

### Modified Capabilities


## Impact

- **Affected code**: `chklog.py` 檔案開頭的路徑設定區塊 (以及需要時可能影響到 `check_excel.py`)。
- **System**: 提升了在地端各種不同作業系統或目錄配置下執行的相容性。使用者只要確保將資料放在 `input_data/` 目錄中，並在專案根目錄執行腳本即可。
