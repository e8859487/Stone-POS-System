"""
Guard tests: ensure DataPack.createPdData() always produces the 24 CSV columns
in their exact order. These columns feed directly into the CSV export — any
change in name or position would silently corrupt customer delivery files.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from DataPack import DataPack

EXPECTED_CSV_COLUMNS = [
    "收件人姓名",
    "收件人電話",
    "收件人手機",
    "收件人地址",
    "代收金額或到付",
    "件數",
    "品名(詳參數表)",
    "備註",
    "訂單編號",
    "希望配達時間((詳參數表))",
    "出貨日期(YYYY / MM / DD)",
    "預定配達日期(YYYY / MM / DD)",
    "溫層((詳參數表))",
    "尺寸((詳參數表))",
    "寄件人姓名",
    "寄件人電話",
    "寄件人手機",
    "寄件人地址",
    "保值金額(20001~10萬之間)",
    "品名說明",
    "是否列印",
    "是否捐贈",
    "統一編號",
    "手機載具",
]


@pytest.fixture
def sample_datapack():
    dp = DataPack()
    dp.name = "測試姓名"
    dp.phone = "04-12345678"
    dp.mPhone = "0912-345-678"
    dp.address = "台中市測試路1號"
    dp.shippingDate = "2026/6/15"
    dp.arrivalDate = "2026/6/16"
    dp.numbersOfPack = "1"
    dp.numbers = "4"
    return dp


def test_csv_column_count(sample_datapack):
    df = sample_datapack.createPdData()
    assert len(df.columns) == 24, f"Expected 24 columns, got {len(df.columns)}"


def test_csv_column_order(sample_datapack):
    df = sample_datapack.createPdData()
    assert list(df.columns) == EXPECTED_CSV_COLUMNS, (
        "CSV column order has changed — this will corrupt the delivery export file.\n"
        f"Expected: {EXPECTED_CSV_COLUMNS}\n"
        f"Got:      {list(df.columns)}"
    )


def test_csv_column_names_unchanged(sample_datapack):
    df = sample_datapack.createPdData()
    actual = set(df.columns)
    expected = set(EXPECTED_CSV_COLUMNS)
    missing = expected - actual
    extra = actual - expected
    assert not missing and not extra, (
        f"CSV columns changed. Missing: {missing}  Extra: {extra}"
    )
