# Tasks: Fix chklog.py Parsing Logic for RPT and XML Files

## 1. Update Path Parsing Logic
- [x] 1.1 In `chklog.py`, locate the `parse_simple_txt` function.
- [x] 1.2 Before checking `p.lower().endswith('.rpt') | .xml`, add logic to strip surrounding whitespace and quotes (`"` and `'`) from the string `p`.


## 2. Update Date Regex and Formatting
- [x] 2.1 In `parse_simple_txt`, locate the `date_pattern` variable.
- [x] 2.2 Update the regex to `r'(20\d{2})[-/](\d{1,2})[-/](\d{1,2})'` to match single-digit months and days.
- [x] 2.3 Update the `date_str` formatting logic to ensure the extracted month and day are padded with leading zeros (e.g., `f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}"`).

## 3. Verification
- [x] 3.1 Run `python chklog.py` against the existing `異動的rpt_xml檔案.txt` and `GP程式修改記錄.xlsx` files.
- [x] 3.2 Verify that the generated output log no longer reports errors for valid `.rpt` and `.xml` files that were previously failing due to the parsing bugs.
