## ADDED Requirements

### Requirement: Dynamically Resolve Project Base Directory
The script SHALL resolve the project base directory dynamically at runtime based on the script's location (`__file__`).

#### Scenario: Script executed from a different working directory
- **WHEN** a user executes `python path/to/project/chklog.py` from outside the project root
- **THEN** the script successfully identifies `path/to/project/` as the base directory

### Requirement: Use Relative Paths for Input and Output Data
The script SHALL construct paths for `input_data` and `output_data` relative to the resolved project base directory.

#### Scenario: Script reads input files
- **WHEN** the script attempts to read the Excel or TXT files
- **THEN** it reads them from the `input_data/` directory located within the dynamically resolved base directory

#### Scenario: Script writes output file
- **WHEN** the script finishes the log checking and attempts to save the report
- **THEN** it creates the output file inside the `output_data/` directory located within the dynamically resolved base directory
