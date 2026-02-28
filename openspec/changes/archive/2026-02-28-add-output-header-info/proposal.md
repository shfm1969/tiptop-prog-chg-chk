## Why

目前 `chklog.py` 產生的稽核報告（`chklog_*.txt`）開頭只有標題和產生時間，缺少所使用的輸入資料檔案資訊。當使用者回頭查閱報告時，無法得知該次稽核使用了哪些輸入檔案，以及這些檔案的最後修改日期。加入這些資訊能大幅提升報告的可追溯性與稽核佐證價值。

## What Changes

- 在輸出報告的開頭區塊（標題與分隔線之後、檢查結果之前）新增一個「輸入資料來源」段落
- 該段落列出三個輸入檔案的檔名與最後修改日期：
  - `GP程式修改記錄.xlsx`
  - `異動的4gl_4fd檔案.txt`
  - `異動的rpt_xml檔案.txt`
- 使用 `os.path.getmtime()` 取得檔案最後修改日期

## Capabilities

### New Capabilities
- `output-header-info`: 在輸出報告開頭顯示輸入資料檔名及其最後修改日期

### Modified Capabilities
（無）

## Impact

- 修改檔案：`chklog.py`（`main()` 函式中的檔案寫入區塊）
- 輸出格式變更：`chklog_*.txt` 報告開頭會多出「輸入資料來源」段落
- 無破壞性變更，不影響既有檢查邏輯
