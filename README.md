# Business Data Integrity Validator

A Python-based data validation tool that simulates real-world ERP/SAP data quality checks. Designed to identify common data integrity issues in business datasets — such as missing values, duplicates, invalid formats, and wrong data types — and generate structured reports for analysis and compliance.

---

## 🎯 Business Problem

In enterprise systems like SAP, poor data quality leads to incorrect reporting, failed transactions, and compliance issues. This tool automates the validation of business records before they are processed — mimicking the data integrity checks performed by SAP analysts.

---

## ✅ Features

| Validation Check | Description |
|---|---|
| Missing Values | Detects null/empty fields across all columns |
| Duplicate Records | Identifies fully repeated rows |
| Invalid Numeric Values | Flags negative or zero quantities/prices |
| Wrong Data Types | Catches text in numeric fields |
| Date Format Validation | Ensures dates follow YYYY-MM-DD standard |

---

## 📁 Project Structure

```
data-integrity-validator/
│
├── validator.py              # Core validation logic
├── sales_data.csv            # Sample business dataset (with intentional errors)
├── validation_report.xlsx    # Generated Excel report (multi-sheet)
├── validation_summary.json   # Generated JSON summary
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
│
└── tests/
    └── test_validator.py     # Automated pytest test suite (20 test cases)
```

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the validator
```bash
python validator.py
```

### 3. Run the test suite
```bash
pytest tests/ -v
```

### 4. Generate HTML test report
```bash
pytest tests/ -v --html=test_report.html
```

---

## 📊 Sample Output

```
✅ Loaded 11 records from 'sales_data.csv'

=======================================================
       BUSINESS DATA INTEGRITY VALIDATION REPORT
=======================================================
  Total Records Scanned : 11
  Total Issues Found    : 8

  Issues by Type:
    • Invalid Numeric Value          3 issue(s)
    • Missing Value                  3 issue(s)
    • Duplicate Record               1 issue(s)
    • Wrong Date Format              1 issue(s)

  Issues by Severity:
    • High        7 issue(s)
    • Medium      1 issue(s)
=======================================================
  Reports saved:
    • validation_report.xlsx
    • validation_summary.json
=======================================================
```

---

## 🛠️ Tech Stack

- **Python** — core logic
- **pandas** — data loading and analysis
- **openpyxl** — Excel report generation
- **pytest** — automated test suite
- **pytest-html** — HTML test reports
- **GitHub Actions** — CI/CD pipeline

---

## 💡 Real-World Relevance

This project mirrors core SAP analyst responsibilities:
- **Data integrity checks** → SAP data migration validation
- **Issue documentation** → SAP defect reporting
- **Automated testing** → SAP UAT (User Acceptance Testing)
- **Report generation** → SAP compliance documentation
