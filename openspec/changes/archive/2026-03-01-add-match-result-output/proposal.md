## Why

目前 `chklog.py` 的稽核報告僅顯示「找不到對應」的異常項目。當所有比對都成功時僅出現「全部符合」訊息，使用者無法確認實際比對到了 Excel 的哪筆資料。新增比對成功的明細輸出，可提升稽核報告的可追溯性與完整性。

## What Changes

- 保留現有的「找不到則顯示異常說明」功能，異常訊息格式不變
- **新增**: 比對成功時，輸出 `[Row序號][程式編號],[上線日期]` 格式的成功明細
- 四個檢查區塊（4gl/global、4fd、rpt、xml）皆須套用此規則

## Capabilities

### New Capabilities
- `match-result-display`: 在稽核報告中顯示比對成功記錄，格式為 `[Row序號][程式編號],[上線日期]`

### Modified Capabilities

(無修改既有 Capability)

## Impact

- 修改 `chklog.py` 中的四個檢查區塊邏輯，於比對成功時記錄並輸出相關資訊
- `output_data/` 下的輸出文字檔內容將增加成功比對的明細行
- 不影響輸入檔案格式或 Excel 欄位結構
