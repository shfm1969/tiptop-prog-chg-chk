# 程式修改紀錄檢查

這是一個用於比對「人工維護的程式修改紀錄 Excel 檔」與「系統自動產生的程式修改紀錄文字檔」的工具專案。
透過此工具，可以快速稽核人工紀錄是否有遺漏或不一致的地方。

## 前置需求 (Prerequisites)

- Python 3.12 
- [uv](https://github.com/astral-sh/uv) (超快 Python 套件與專案管理工具)

## 環境安裝與建置 (Installation)

本專案使用 `uv` 來管理 Python 環境與相依套件。

1. **安裝 uv** (如果尚未安裝):
   請參考 [uv 官方文件](https://docs.astral.sh/uv/getting-started/installation/) 安裝。
   在 Windows 的 PowerShell 可使用以下指令：
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```

2. **同步專案環境**:
   在專案根目錄下執行以下指令，`uv` 會自動建立虛擬環境 (於 `.venv` 目料下) 並安裝 `pyproject.toml` 中的所有套件：
   ```bash
   uv sync
   ```

## 目錄結構 (Directory Structure)

- `input_data/`: 用來放置待檢查的原始資料，包含人工維護的 Excel (`.xlsx`) 以及系統產生的紀錄檔 (`.txt`)。
- `output_data/`: 腳本執行後的分析結果與比對報表會輸出至此資料夾。
- `原始資料/`: （可選）存放未處理前的原始來源檔案備份。
- `chklog.py`: 主要的主程式，執行完整的檢核邏輯並產出稽核報告。
- `check_excel.py`: 負責處理 Excel 解析的輔助腳本。

## 使用方式 (Usage)

### 1. 準備輸入資料

將您的檔案放置到 `input_data/` 目錄中。請確認檔案名稱與格式符合以下要求（您也可以根據需要修改 `chklog.py` 內的預設路徑）：
- **Excel 紀錄檔**：預設為 `input_data/GP程式修改記錄.xlsx`（請確保檔案內只有一個工作表，且包含「程式上線日」、「程式編號」、「改程式」、「改畫面」、「改rpt」、「改xml」等欄位）。
- **文字紀錄檔**：
  - `input_data/異動的4gl_4fd檔案.txt` (包含 `ls -l` 格式的 .4gl 與 .4fd 檔案列表)
  - `input_data/異動的rpt_xml檔案.txt` (包含 .rpt 與 .xml 檔案的修改紀錄)

### 2. 執行稽核腳本

在設定好的環境中，執行以下指令啟動檢查：
```bash
uv run python chklog.py
```

### 3. 查看稽核報告

執行完成後，系統會在終端機顯示「稽核完成！報告已儲存至: ...」的訊息。
請前往 `output_data/` 目錄，您會看到以執行時間命名的文字檔（例如：`chklog_20260228_154100.txt`）。
打開該檔案即可查看詳細的稽核結果，報告中會列出沒有在 Excel 紀錄中找到對應項目（或日期不符、未打勾等）的異常檔案。
