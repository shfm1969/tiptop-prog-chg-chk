import pandas as pd
import sys
try:
    xls = pd.ExcelFile(r'd:\AI_Study\1.study_by_antigravity\程式修改紀錄檢查\input_data\附件一 02.GP程式修改記錄v20260223.xlsx')
    print('Sheets:', xls.sheet_names)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    print('Columns:', list(df.columns))
    print(df.head(5).to_string())
except Exception as e:
    print(e, file=sys.stderr)
