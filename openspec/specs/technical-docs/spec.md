## ADDED Requirements

### Requirement: Provide Environment Setup Instructions
The documentation SHALL include instructions on how to set up the development and execution environment using `uv` and Python.

#### Scenario: New developer sets up project
- **WHEN** a new developer clones the repository
- **THEN** they can follow the instructions to successfully install dependencies (`uv sync` or equivalent) and run the scripts

### Requirement: Document Script Usage
The documentation SHALL explain the purpose, inputs, outputs, and usage of the main scripts (`chklog.py`, `check_excel.py`).

#### Scenario: User runs chklog.py
- **WHEN** a user wants to check the program modification logs
- **THEN** they can look up the command in the README and run `uv run python chklog.py` successfully

### Requirement: Explain Directory Structure
The documentation SHALL outline the purpose of key directories like `input_data`, `output_data`, and `原始資料`.

#### Scenario: User places input files
- **WHEN** a user prepares to run the log check
- **THEN** they know exactly which folder to put the Excel and text files in based on the directory structure documentation
