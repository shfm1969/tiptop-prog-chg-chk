# Design: Fix chklog.py Parsing Logic for RPT and XML Files

## Context

The `chklog.py` script needs to extract file paths and modification dates from a text file (`異動的rpt_xml檔案.txt`). The current implementation fails because it doesn't account for quotes and double quotes surrounding file paths, and its date regex is too strict regarding single-digit dates.

## Goals / Non-Goals

**Goals:**
*   Correctly parse dates with single-digit months or days (e.g., `2026/2/5`).
*   Correctly parse file paths enclosed in double quotes.

**Non-Goals:**
*   Refactor the entire `chklog.py` script.
*   Change how Excel matching works.

## Proposed Solution

Modify the `parse_simple_txt` function in `chklog.py`:

**1. Clean the File Path String:**
Before checking the file extension, strip any surrounding whitespace and quotes (`"` or `'`) from the path string.
```python
p_clean = p.strip('\"\'')
if p_clean.lower().endswith('.rpt') or p_clean.lower().endswith('.xml'):
    # ...
```

**2. Update the Date Regular Expression:**
Change the regex to allow 1 or 2 digits for the month and day.
```python
# Old:
# date_pattern = re.compile(r'(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])')

# New:
date_pattern = re.compile(r'(20\d{2})[-/](\d{1,2})[-/](\d{1,2})')
```

**3. Format the Extracted Date:**
When a date is matched using the new regex, format it with leading zeros to ensure it matches the `YYYY-MM-DD` format expected later in the script.
```python
if date_match:
    date_str = f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}"
```

## Risks / Trade-offs

*   **Risk:** The looser date regex might accidentally match unintended strings if the text file format changes significantly.
*   **Trade-off:** Minimal risk, as the script already expects standard date representations and the new regex just accommodating missing leading zeros.
