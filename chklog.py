import pandas as pd
import re
import os
from datetime import datetime
import sys

# 檔案路徑設定
# 動態取得專案根目錄 (即本腳本所在的資料夾)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_PATH = os.path.join(BASE_DIR, 'input_data', 'GP程式修改記錄.xlsx')
TXT_4GL_4FD = os.path.join(BASE_DIR, 'input_data', '異動的4gl_4fd檔案.txt')
TXT_RPT_XML = os.path.join(BASE_DIR, 'input_data', '異動的rpt_xml檔案.txt')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_data')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_ls_l_txt(filepath):
    results = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split()
            perm_idx = -1
            for i, p in enumerate(parts):
                if p.startswith('-r') or p.startswith('dr'):
                    perm_idx = i
                    break
            if perm_idx != -1 and len(parts) > perm_idx + 8:
                month = parts[perm_idx + 5]
                day = parts[perm_idx + 6]
                filepath_raw = parts[perm_idx + 8]
                filename = os.path.basename(filepath_raw)
                
                month_map = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
                             'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
                m_num = month_map.get(month, '01')
                d_num = f"{int(day):02d}"
                current_year = datetime.now().year
                date_str = f"{current_year}-{m_num}-{d_num}"
                
                results.append({
                    'original': line,
                    'date_str': date_str,
                    'filename': filename,
                    'filepath': filepath_raw
                })
    return results

def parse_simple_txt(filepath):
    results = []
    date_pattern = re.compile(r'(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])')
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('D:\\') or line.startswith('請按任意鍵') or line.startswith('type '):
                continue
            fname = ""
            parts = re.split(r'[\s,]+', line)
            for p in parts:
                if p.lower().endswith('.rpt') or p.lower().endswith('.xml'):
                    fname = os.path.basename(p)
                    break
            if not fname: continue
            date_match = date_pattern.search(line)
            date_str = ""
            if date_match:
                date_str = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
            else:
                perm_idx = -1
                for i, p in enumerate(parts):
                    if p.startswith('-r') or p.startswith('dr'):
                        perm_idx = i
                        break
                if perm_idx != -1 and len(parts) > perm_idx + 6:
                    month = parts[perm_idx + 5]
                    day = parts[perm_idx + 6]
                    month_map = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
                                 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
                    m_num = month_map.get(month, '01')
                    if day.isdigit():
                        d_num = f"{int(day):02d}"
                        current_year = datetime.now().year
                        date_str = f"{current_year}-{m_num}-{d_num}"
            if not date_str: date_str = "UNKNOWN_DATE"
            results.append({
                'original': line,
                'date_str': date_str,
                'filename': fname,
            })
    return results

def is_checked(val):
    """檢查打勾是否為 Y (忽略大小寫)"""
    if pd.isnull(val): return False
    return str(val).strip().upper() == 'Y'

def extract_base_prog_id(ex_code):
    """
    (6)的類似檔名比對,以xlsx檔的[程式編號]為準,參考規則如下
    (5.1)xlsx檔的[程式編號]="axmt400",在(2)(3)(4)中的檔名包含"axmt400"就算有
    (5.2)xlsx檔的[程式編號]="saxmt400",在(2)(3)(4)中的檔名包含"axmt400"就算有
    (5.3)xlsx檔的[程式編號]="saxmt400_sub",在(2)(3)(4)中的檔名包含"axmt400"就算有
    """
    ex_code = str(ex_code).lower().strip()
    if not ex_code:
        return ""
    # 拔掉 's' 開頭
    if ex_code.startswith('s'):
        ex_code = ex_code[1:]
    # 拔掉 '_sub' (或其它 _ 後綴)
    if '_' in ex_code:
        ex_code = ex_code.split('_')[0]
    return ex_code

def is_similar_prog_id(ex_code, fname_base):
    ex_code_clean = extract_base_prog_id(ex_code)
    if ex_code_clean and ex_code_clean in fname_base.lower():
        return True
    return False

def main():
    try:
        # --- 檢查 Excel 是否只包含一個工作表 (Sheet) ---
        xl = pd.ExcelFile(EXCEL_PATH)
        if len(xl.sheet_names) > 1:
            print(f"失敗！Excel 檔案 '{os.path.basename(EXCEL_PATH)}' 包含多個工作表 {xl.sheet_names}，請確保只能有一個頁面。")
            return
            
        df_excel = pd.read_excel(EXCEL_PATH, header=1)
        df_excel.columns = [str(c).replace('\n', '').strip() for c in df_excel.columns]
        
        col_date = '程式上線日'
        col_prog = '程式編號'
        col_chk_prog = '改程式'
        col_chk_ui = '改畫面'
        col_chk_rpt = '改rpt'
        col_chk_xml = '改xml'
        
        def format_date(val):
            if pd.isnull(val): return ""
            if isinstance(val, pd.Timestamp) or isinstance(val, datetime):
                return val.strftime('%Y-%m-%d')
            s = str(val).split(' ')[0]
            s = s.replace('/', '-')
            return s
            
        df_excel['上線日期_str'] = df_excel[col_date].apply(format_date)
        df_excel['程式編號_lower'] = df_excel[col_prog].astype(str).str.lower().fillna("")

        list_4gl_4fd = parse_ls_l_txt(TXT_4GL_4FD)
        list_rpt_xml = parse_simple_txt(TXT_RPT_XML)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_file = os.path.join(OUTPUT_DIR, f'chklog_{timestamp}.txt')
        
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(f"程式修改紀錄稽核報告 - 產生時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")

            # === (1) 檢查 *.4gl 及 *.global (精確比對) ===
            f.write("=== 檢查 (1): *.4gl / *.global 檔案 ===\n")
            f.write("規則：依修改日期比對 Excel[程式上線日]，需[程式編號]明確相同(忽略副檔名)，且[改程式]欄位為Y\n")
            f.write("-" * 60 + "\n")
            missing_1 = []
            for item in list_4gl_4fd:
                fname = item['filename'].lower()
                f_date = item['date_str']
                
                if fname.endswith('.4gl') or fname.endswith('.global'):
                    base_name = os.path.splitext(fname)[0] 
                    
                    found = False
                    for _, row in df_excel.iterrows():
                        ex_code = str(row['程式編號_lower'])
                        ex_date = row['上線日期_str']
                        chk = is_checked(row.get(col_chk_prog, ''))
                        
                        if ex_code == base_name and ex_date == f_date and chk:
                            found = True
                            break
                    
                    if not found:
                        missing_1.append(f"[{f_date}] {fname} -> 異常! Excel 中找不到明確相同的[程式編號]，或修改日期不同，或[改程式]未標示Y")
                        
            if not missing_1: f.write("=> 全部符合！\n")
            else:
                for m in missing_1: f.write(m + "\n")
            f.write("\n")


            # === (2) 檢查 *.4fd 檔案 (類似比對) ===
            f.write("=== 檢查 (2): *.4fd 檔案 ===\n")
            f.write("規則：依修改日期比對 Excel[程式上線日]，需[程式編號]透過規則包含在內，且[改畫面]欄位為Y\n")
            f.write("-" * 60 + "\n")
            missing_2 = []
            for item in list_4gl_4fd:
                fname = item['filename'].lower()
                f_date = item['date_str']
                
                if fname.endswith('.4fd'):
                    base_name = os.path.splitext(fname)[0]
                    found = False
                    for _, row in df_excel.iterrows():
                        ex_code = str(row['程式編號_lower'])
                        ex_date = row['上線日期_str']
                        chk = is_checked(row.get(col_chk_ui, ''))
                        
                        if is_similar_prog_id(ex_code, base_name):
                            if ex_date == f_date and chk:
                                found = True
                                break
                    
                    if not found:
                         missing_2.append(f"[{f_date}] {fname} -> 異常! Excel 中找不到類似的[程式編號]，或修改日期不同，或[改畫面]未標示Y")

            if not missing_2: f.write("=> 全部符合！\n")
            else:
                for m in missing_2: f.write(m + "\n")
            f.write("\n")


            # === (3) 檢查 *.rpt 檔案 (類似比對) ===
            f.write("=== 檢查 (3): *.rpt 檔案 ===\n")
            f.write("規則：依修改日期比對 Excel[程式上線日]，需[程式編號]透過規則包含在內，且[改rpt]欄位為Y\n")
            f.write("-" * 60 + "\n")
            missing_3 = []
            for item in list_rpt_xml:
                fname = item['filename'].lower()
                f_date = item['date_str']
                
                if fname.endswith('.rpt'):
                    base_name = os.path.splitext(fname)[0]
                    found = False
                    for _, row in df_excel.iterrows():
                        ex_code = str(row['程式編號_lower'])
                        ex_date = row['上線日期_str']
                        chk = is_checked(row.get(col_chk_rpt, ''))
                        
                        if is_similar_prog_id(ex_code, base_name):
                            if ex_date == f_date and chk:
                                found = True
                                break
                    if not found:
                        missing_3.append(f"[{f_date}] {fname} -> 異常! Excel 中找不到類似的[程式編號]，或修改日期不同，或[改rpt]未標示Y")

            if not missing_3: f.write("=> 全部符合！\n")
            else:
                for m in missing_3: f.write(m + "\n")
            f.write("\n")


            # === (4) 檢查 *.xml 檔案 (類似比對) ===
            f.write("=== 檢查 (4): *.xml 檔案 ===\n")
            f.write("規則：依修改日期比對 Excel[程式上線日]，需[程式編號]透過規則包含在內，且[改xml]欄位為Y\n")
            f.write("-" * 60 + "\n")
            missing_4 = []
            for item in list_rpt_xml:
                fname = item['filename'].lower()
                f_date = item['date_str']
                
                if fname.endswith('.xml'):
                    base_name = os.path.splitext(fname)[0]
                    found = False
                    for _, row in df_excel.iterrows():
                        ex_code = str(row['程式編號_lower'])
                        ex_date = row['上線日期_str']
                        chk = is_checked(row.get(col_chk_xml, ''))
                        
                        if is_similar_prog_id(ex_code, base_name):
                            if ex_date == f_date and chk:
                                found = True
                                break
                    if not found:
                        missing_4.append(f"[{f_date}] {fname} -> 異常! Excel 中找不到類似的[程式編號]，或修改日期不同，或[改xml]未標示Y")

            if not missing_4: f.write("=> 全部符合！\n")
            else:
                for m in missing_4: f.write(m + "\n")
            f.write("\n")

        print(f"稽核完成！報告已儲存至: {out_file}")

    except Exception as e:
        print(f"執行發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
