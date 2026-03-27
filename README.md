# 程式修改紀錄檢查 (tiptop-prog-chg-chk)

一個用於比對「人工維護的程式修改紀錄 Excel 檔」與「系統自動產生的程式異動文字檔」的稽核工具。
透過此工具，可以快速檢核人工紀錄是否有遺漏或不一致的地方，產出完整的稽核報告。

---

## 功能特色 (Features)

- **多類型檔案比對**：支援 `.4gl`、`.global`、`.4fd`、`.rpt`、`.xml` 五種副檔名的異動比對。
- **精確 & 模糊比對**：
  - `.4gl` / `.global`：以精確的「程式編號」比對。
  - `.4fd` / `.rpt` / `.xml`：以模糊規則比對（自動去除前綴 `s`、後綴 `_sub` 等）。
- **自動日期比對**：將系統檔案清單中的修改日期與 Excel「程式上線日」進行交叉驗證。
- **勾選欄位檢核**：依據檔案類型對應檢查「改程式」、「改畫面」、「改rpt」、「改xml」是否標示為 `Y`。
- **稽核報告自動產出**：報告以時間戳命名，儲存至 `output_data/` 目錄，內容包含比對成功與比對異常的明細。
- **動態路徑**：使用腳本所在目錄作為基準，不綁定特定絕對路徑，具有可攜性。

---

## 前置需求 (Prerequisites)

- **Python** ≥ 3.11
- [**uv**](https://github.com/astral-sh/uv) — 超快 Python 套件與專案管理工具

---

## 環境安裝與建置 (Installation)

本專案使用 `uv` 來管理 Python 環境與相依套件。

1. **安裝 uv**（如果尚未安裝）：
   請參考 [uv 官方文件](https://docs.astral.sh/uv/getting-started/installation/)。
   Windows PowerShell:
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```

2. **同步專案環境**：
   在專案根目錄下執行，`uv` 會自動建立虛擬環境 (`.venv`) 並安裝所有相依套件：
   ```bash
   uv sync
   ```

---

## 目錄結構 (Directory Structure)

```
tiptop-prog-chg-chk/
├── .agent/                 # AI Agent 專屬設定與相關腳本
├── chklog.py              # 主程式 — 執行完整的檢核邏輯並產出稽核報告
├── pyproject.toml          # 專案設定 & 相依套件定義
├── uv.lock                 # 套件版本鎖定檔 (uv 管理)
├── .python-version         # 指定 Python 版本
├── README.md
├── .gitignore
├── input_data/             # 輸入資料 (Excel + 系統清單文字檔) (已排除於 Git 追蹤)
│   ├── GP程式修改記錄.xlsx
│   ├── 異動的4gl_4fd檔案.txt
│   └── 異動的rpt_xml檔案.txt
├── input_data_sample/      # 範例輸入資料
├── output_data/            # 稽核報告輸出 (已排除於 Git 追蹤)
├── openspec/               # OpenSpec 變更管理紀錄與技術規格
├── 原始資料/                # 原始來源檔案備份 (已排除於 Git 追蹤)
├── 對話歷史.md             # 專案過程對話彙覽
└── 對話紀錄/               # 歷史對話細節
```

---

## 使用方式 (Usage)

### 1. 準備輸入資料

將檔案放置到 `input_data/` 目錄：

| 檔案 | 說明 |
|------|------|
| `GP程式修改記錄.xlsx` | 人工維護的程式修改 Excel 紀錄。須只有一個工作表，且包含「程式上線日」、「程式編號」、「改程式」、「改畫面」、「改rpt」、「改xml」等欄位。 |
| `異動的4gl_4fd檔案.txt` | 系統產生的 `ls -l` 格式清單，包含 `.4gl`、`.global`、`.4fd` 檔案資訊。 |
| `異動的rpt_xml檔案.txt` | 系統產生的 `.rpt` 與 `.xml` 修改紀錄。 |

### 2. 執行稽核腳本

```bash
uv run python chklog.py
```

### 3. 查看稽核報告

執行完成後，終端機會顯示：
```
稽核完成！報告已儲存至: output_data/chklog_YYYYMMDD_HHMMSS.txt
```

報告包含以下四個檢查區塊：

| 檢查 | 比對對象 | 比對方式 | 檢核欄位 |
|------|----------|----------|----------|
| 檢查 (1) | `*.4gl` / `*.global` | 精確比對 — 程式編號須完全相同 | 改程式 = Y |
| 檢查 (2) | `*.4fd` | 模糊比對 — 去除前綴 `s`、後綴 `_sub` 等 | 改畫面 = Y |
| 檢查 (3) | `*.rpt` | 模糊比對 | 改rpt = Y |
| 檢查 (4) | `*.xml` | 模糊比對 | 改xml = Y |

每個檢查區塊列出「**比對成功**」與「**比對異常**」兩類結果，方便快速定位需要關注的異常項目。

---

## 比對規則說明

### 精確比對（適用於 `.4gl` / `.global`）
- 檔案名稱（去除副檔名後）必須與 Excel「程式編號」**完全一致**。
- 修改日期必須與 Excel「程式上線日」相同。

### 模糊比對（適用於 `.4fd` / `.rpt` / `.xml`）
- 支援以下命名衍生規則：
  - `axmt400` ⟵ 直接包含即符合
  - `saxmt400` ⟵ 自動去除前綴 `s` 再比對
  - `saxmt400_sub` ⟵ 自動去除前綴 `s` 及後綴 `_sub` 再比對
- 修改日期必須與 Excel「程式上線日」相同。

---

## 相依套件 (Dependencies)

| 套件 | 用途 |
|------|------|
| `pandas` ≥ 3.0.1 | 讀取 Excel 及資料處理 |
| `openpyxl` ≥ 3.1.5 | Excel `.xlsx` 格式支援 |

---

## 授權 (License)

本專案目前尚未指定授權條款。
