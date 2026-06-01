"""
Test Suite — Business Data Integrity Validator
-----------------------------------------------
Automated tests for each validation check using pytest.
Mirrors real-world SAP UAT (User Acceptance Testing) practices.
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from validator import (
    check_missing_values,
    check_duplicate_records,
    check_negative_or_zero_values,
    check_invalid_data_types,
    check_date_format,
)


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def clean_df():
    """A perfectly clean dataset — no issues expected."""
    return pd.DataFrame({
        "OrderID"     : [1001, 1002, 1003],
        "CustomerName": ["Amit", "Priya", "Rahul"],
        "Product"     : ["Laptop", "Mouse", "Keyboard"],
        "Quantity"    : [1, 2, 3],
        "Price"       : [45000, 500, 1200],
        "OrderDate"   : ["2024-01-15", "2024-01-16", "2024-01-17"],
        "Region"      : ["North", "South", "East"],
    })


@pytest.fixture
def missing_df():
    """Dataset with missing values."""
    return pd.DataFrame({
        "OrderID"     : [1001, 1002],
        "CustomerName": [None, "Priya"],   # missing name
        "Product"     : ["Laptop", "Mouse"],
        "Quantity"    : [1, 2],
        "Price"       : [45000, 500],
        "OrderDate"   : ["2024-01-15", "2024-01-16"],
        "Region"      : ["North", None],   # missing region
    })


@pytest.fixture
def duplicate_df():
    """Dataset with a duplicate row."""
    return pd.DataFrame({
        "OrderID"     : [1001, 1001],
        "CustomerName": ["Amit", "Amit"],
        "Product"     : ["Laptop", "Laptop"],
        "Quantity"    : [2, 2],
        "Price"       : [45000, 45000],
        "OrderDate"   : ["2024-01-15", "2024-01-15"],
        "Region"      : ["North", "North"],
    })


@pytest.fixture
def negative_df():
    """Dataset with negative/zero numeric values."""
    return pd.DataFrame({
        "OrderID"     : [1001, 1002, 1003],
        "CustomerName": ["Amit", "Priya", "Rahul"],
        "Product"     : ["Laptop", "Mouse", "Keyboard"],
        "Quantity"    : [-1, 0, 3],        # negative & zero
        "Price"       : [45000, -500, 1200],  # negative price
        "OrderDate"   : ["2024-01-15", "2024-01-16", "2024-01-17"],
        "Region"      : ["North", "South", "East"],
    })


@pytest.fixture
def wrong_type_df():
    """Dataset with wrong data types in numeric columns."""
    return pd.DataFrame({
        "OrderID"     : [1001, 1002],
        "CustomerName": ["Amit", "Priya"],
        "Product"     : ["Laptop", "Mouse"],
        "Quantity"    : ["abc", 2],        # 'abc' is not a number
        "Price"       : [45000, 500],
        "OrderDate"   : ["2024-01-15", "2024-01-16"],
        "Region"      : ["North", "South"],
    })


@pytest.fixture
def wrong_date_df():
    """Dataset with incorrectly formatted dates."""
    return pd.DataFrame({
        "OrderID"     : [1001, 1002],
        "CustomerName": ["Amit", "Priya"],
        "Product"     : ["Laptop", "Mouse"],
        "Quantity"    : [1, 2],
        "Price"       : [45000, 500],
        "OrderDate"   : ["15-01-2024", "2024-01-16"],  # wrong format
        "Region"      : ["North", "South"],
    })


# ─────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────

class TestMissingValues:
    def test_no_issues_on_clean_data(self, clean_df):
        issues = check_missing_values(clean_df)
        assert len(issues) == 0, "Clean data should have no missing value issues"

    def test_detects_missing_customer_name(self, missing_df):
        issues = check_missing_values(missing_df)
        columns_flagged = [i["Column"] for i in issues]
        assert "CustomerName" in columns_flagged

    def test_detects_missing_region(self, missing_df):
        issues = check_missing_values(missing_df)
        columns_flagged = [i["Column"] for i in issues]
        assert "Region" in columns_flagged

    def test_severity_is_high(self, missing_df):
        issues = check_missing_values(missing_df)
        assert all(i["Severity"] == "High" for i in issues)


class TestDuplicateRecords:
    def test_no_issues_on_clean_data(self, clean_df):
        issues = check_duplicate_records(clean_df)
        assert len(issues) == 0

    def test_detects_duplicate_row(self, duplicate_df):
        issues = check_duplicate_records(duplicate_df)
        assert len(issues) >= 1

    def test_duplicate_check_label(self, duplicate_df):
        issues = check_duplicate_records(duplicate_df)
        assert issues[0]["Check"] == "Duplicate Record"


class TestNegativeValues:
    def test_no_issues_on_clean_data(self, clean_df):
        issues = check_negative_or_zero_values(clean_df)
        assert len(issues) == 0

    def test_detects_negative_quantity(self, negative_df):
        issues = check_negative_or_zero_values(negative_df)
        columns_flagged = [i["Column"] for i in issues]
        assert "Quantity" in columns_flagged

    def test_detects_negative_price(self, negative_df):
        issues = check_negative_or_zero_values(negative_df)
        columns_flagged = [i["Column"] for i in issues]
        assert "Price" in columns_flagged

    def test_detects_zero_quantity(self, negative_df):
        issues = check_negative_or_zero_values(negative_df)
        zero_issues = [i for i in issues if str(i["Found Value"]) == "0"]
        assert len(zero_issues) >= 1


class TestDataTypes:
    def test_no_issues_on_clean_data(self, clean_df):
        issues = check_invalid_data_types(clean_df)
        assert len(issues) == 0

    def test_detects_text_in_quantity(self, wrong_type_df):
        issues = check_invalid_data_types(wrong_type_df)
        columns_flagged = [i["Column"] for i in issues]
        assert "Quantity" in columns_flagged

    def test_severity_is_medium(self, wrong_type_df):
        issues = check_invalid_data_types(wrong_type_df)
        assert all(i["Severity"] == "Medium" for i in issues)


class TestDateFormat:
    def test_no_issues_on_clean_data(self, clean_df):
        issues = check_date_format(clean_df)
        assert len(issues) == 0

    def test_detects_wrong_date_format(self, wrong_date_df):
        issues = check_date_format(wrong_date_df)
        assert len(issues) >= 1

    def test_correct_column_flagged(self, wrong_date_df):
        issues = check_date_format(wrong_date_df)
        assert issues[0]["Column"] == "OrderDate"

    def test_wrong_value_captured(self, wrong_date_df):
        issues = check_date_format(wrong_date_df)
        assert issues[0]["Found Value"] == "15-01-2024"
