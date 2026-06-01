"""
Business Data Integrity Validator
----------------------------------
Simulates real-world ERP/SAP data validation by checking
business records for common data quality issues.

Author: Shristi Sharma
"""

import pandas as pd
from datetime import datetime
import json


def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV data into a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} records from '{filepath}'\n")
    return df


# ─────────────────────────────────────────────
# VALIDATION CHECKS
# ─────────────────────────────────────────────

def check_missing_values(df: pd.DataFrame) -> list:
    """Check for missing/null values in any column."""
    issues = []
    for col in df.columns:
        missing_rows = df[df[col].isnull()].index.tolist()
        for row in missing_rows:
            issues.append({
                "Check"      : "Missing Value",
                "Row"        : row + 2,       # +2 for header & 0-index
                "Column"     : col,
                "Found Value": "NULL / Empty",
                "Severity"   : "High"
            })
    return issues


def check_duplicate_records(df: pd.DataFrame) -> list:
    """Check for fully duplicate rows."""
    issues = []
    duplicates = df[df.duplicated(keep=False)]
    seen = set()
    for idx, row in duplicates.iterrows():
        key = tuple(row)
        if key not in seen:
            seen.add(key)
        else:
            issues.append({
                "Check"      : "Duplicate Record",
                "Row"        : idx + 2,
                "Column"     : "All Columns",
                "Found Value": f"OrderID {row.get('OrderID', 'N/A')}",
                "Severity"   : "High"
            })
    return issues


def check_negative_or_zero_values(df: pd.DataFrame) -> list:
    """Check for invalid negative or zero values in numeric columns."""
    issues = []
    numeric_cols = {"Quantity": 0, "Price": 0}   # min allowed value (exclusive)

    for col, min_val in numeric_cols.items():
        if col not in df.columns:
            continue
        numeric_series = pd.to_numeric(df[col], errors="coerce")
        bad_rows = df[(numeric_series <= min_val)].index.tolist()
        for row in bad_rows:
            issues.append({
                "Check"      : "Invalid Numeric Value",
                "Row"        : row + 2,
                "Column"     : col,
                "Found Value": df.at[row, col],
                "Severity"   : "High"
            })
    return issues


def check_invalid_data_types(df: pd.DataFrame) -> list:
    """Check that numeric columns contain only numbers."""
    issues = []
    numeric_cols = ["Quantity", "Price"]

    for col in numeric_cols:
        if col not in df.columns:
            continue
        for idx, val in df[col].items():
            converted = pd.to_numeric(val, errors="coerce")
            if pd.isnull(converted):
                issues.append({
                    "Check"      : "Wrong Data Type",
                    "Row"        : idx + 2,
                    "Column"     : col,
                    "Found Value": val,
                    "Severity"   : "Medium"
                })
    return issues


def check_date_format(df: pd.DataFrame, date_col: str = "OrderDate",
                       expected_format: str = "%Y-%m-%d") -> list:
    """Check that dates follow the expected format."""
    issues = []
    if date_col not in df.columns:
        return issues

    for idx, val in df[date_col].items():
        if pd.isnull(val):
            continue
        try:
            datetime.strptime(str(val).strip(), expected_format)
        except ValueError:
            issues.append({
                "Check"      : "Wrong Date Format",
                "Row"        : idx + 2,
                "Column"     : date_col,
                "Found Value": val,
                "Severity"   : "Medium"
            })
    return issues


# ─────────────────────────────────────────────
# RUN ALL CHECKS
# ─────────────────────────────────────────────

def run_all_checks(df: pd.DataFrame) -> pd.DataFrame:
    """Run all validation checks and return a combined issues DataFrame."""
    all_issues = []
    all_issues += check_missing_values(df)
    all_issues += check_duplicate_records(df)
    all_issues += check_negative_or_zero_values(df)
    all_issues += check_invalid_data_types(df)
    all_issues += check_date_format(df)

    issues_df = pd.DataFrame(all_issues)
    return issues_df


# ─────────────────────────────────────────────
# SUMMARY REPORT
# ─────────────────────────────────────────────

def print_summary(df: pd.DataFrame, issues_df: pd.DataFrame):
    """Print a clean summary to the console."""
    print("=" * 55)
    print("       BUSINESS DATA INTEGRITY VALIDATION REPORT")
    print("=" * 55)
    print(f"  Total Records Scanned : {len(df)}")
    print(f"  Total Issues Found    : {len(issues_df)}")

    if not issues_df.empty:
        print(f"\n  Issues by Type:")
        for check, count in issues_df["Check"].value_counts().items():
            print(f"    • {check:<30} {count} issue(s)")

        print(f"\n  Issues by Severity:")
        for sev, count in issues_df["Severity"].value_counts().items():
            print(f"    • {sev:<10} {count} issue(s)")

    print("=" * 55)
    print("  Reports saved:")
    print("    • validation_report.xlsx")
    print("    • validation_summary.json")
    print("=" * 55)


def save_excel_report(df: pd.DataFrame, issues_df: pd.DataFrame,
                       output_path: str = "validation_report.xlsx"):
    """Save original data + issues into a multi-sheet Excel report."""
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Original Data", index=False)
        if not issues_df.empty:
            issues_df.to_excel(writer, sheet_name="Issues Found", index=False)

            # Summary sheet
            summary = issues_df["Check"].value_counts().reset_index()
            summary.columns = ["Issue Type", "Count"]
            summary.to_excel(writer, sheet_name="Summary", index=False)

    print(f"\n📊 Excel report saved → {output_path}")


def save_json_summary(df: pd.DataFrame, issues_df: pd.DataFrame,
                       output_path: str = "validation_summary.json"):
    """Save a JSON summary for further processing or API integration."""
    summary = {
        "total_records"  : len(df),
        "total_issues"   : len(issues_df),
        "issues_by_type" : issues_df["Check"].value_counts().to_dict() if not issues_df.empty else {},
        "issues_by_severity": issues_df["Severity"].value_counts().to_dict() if not issues_df.empty else {},
        "data_quality_score": round((1 - len(issues_df) / max(len(df), 1)) * 100, 2)
    }
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"📋 JSON summary saved  → {output_path}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    df = load_data("sales_data.csv")
    issues_df = run_all_checks(df)
    print_summary(df, issues_df)
    save_excel_report(df, issues_df)
    save_json_summary(df, issues_df)
