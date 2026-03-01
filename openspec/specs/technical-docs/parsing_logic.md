# Specification: Parsing Logic for chklog.py

## Overview
This specification defines the expected behavior of the `chklog.py` script when parsing file paths and dates from the `異動的rpt_xml檔案.txt` audit file.

## Requirements

### Requirement: Accurately Parse Quoted File Paths
- **GIVEN** a file path string containing double quotes or single quotes (e.g., `"D:\path\to\file.rpt"`).
- **WHEN** the script evaluates the file extension.
- **THEN** it must successfully identify the extension `.rpt` or `.xml` by ignoring the surrounding quotes.

### Requirement: Accurately Parse Single-digit Dates
- **GIVEN** a date string formatted with single digits for the month or day (e.g., `2026/2/5`).
- **WHEN** the script extracts the date.
- **THEN** it must successfully parse the date and format it with leading zeros (e.g., `2026-02-05`) to enable accurate sorting and matching.
