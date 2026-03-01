## ADDED Requirements

### Requirement: 比對成功時顯示 Excel 明細
當 txt 檔案清單中的檔案在 Excel 中找到對應記錄時，系統 SHALL 在稽核報告中輸出成功比對的明細，格式為 `[Row序號][程式編號],[上線日期]`。

#### Scenario: 4gl 檔案比對成功
- **WHEN** `*.4gl` 或 `*.global` 檔案在 Excel 中找到程式編號完全相同、上線日期相符、且「改程式」欄位為 Y 的記錄
- **THEN** 報告 SHALL 輸出該筆成功明細，格式為 `[Row序號][程式編號],[上線日期]`

#### Scenario: 4fd 檔案比對成功
- **WHEN** `*.4fd` 檔案在 Excel 中找到程式編號透過類似比對規則包含在內、上線日期相符、且「改畫面」欄位為 Y 的記錄
- **THEN** 報告 SHALL 輸出該筆成功明細，格式為 `[Row序號][程式編號],[上線日期]`

#### Scenario: rpt 檔案比對成功
- **WHEN** `*.rpt` 檔案在 Excel 中找到程式編號透過類似比對規則包含在內、上線日期相符、且「改rpt」欄位為 Y 的記錄
- **THEN** 報告 SHALL 輸出該筆成功明細，格式為 `[Row序號][程式編號],[上線日期]`

#### Scenario: xml 檔案比對成功
- **WHEN** `*.xml` 檔案在 Excel 中找到程式編號透過類似比對規則包含在內、上線日期相符、且「改xml」欄位為 Y 的記錄
- **THEN** 報告 SHALL 輸出該筆成功明細，格式為 `[Row序號][程式編號],[上線日期]`

### Requirement: 保留異常輸出功能
系統 SHALL 保留現有的異常輸出功能，當檔案在 Excel 中找不到對應記錄時，仍顯示異常說明訊息。

#### Scenario: 比對失敗時顯示異常
- **WHEN** txt 檔案清單中的檔案在 Excel 中找不到對應記錄
- **THEN** 報告 SHALL 輸出異常訊息，格式與現有邏輯一致

### Requirement: Row 序號對應 Excel 實際行號
`[Row序號]` SHALL 對應 Excel 檔案中的實際行號（包含標題列偏移），讓使用者可直接在 Excel 中定位該筆資料。

#### Scenario: Row 序號正確對應
- **WHEN** 比對成功的記錄位於 Excel 資料的第 N 行（pandas index 為 i）
- **THEN** 輸出的 Row 序號 SHALL 為 `i + 3`（因 Excel 標題在第 2 列，資料從第 3 列開始，pandas 0-based）
