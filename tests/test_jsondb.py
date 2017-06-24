import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..")))
TEST_PATH = os.path.join(os.path.abspath(__file__), "..")
TEST_DATA_PATH = os.path.join(TEST_PATH, "testdata.json")

from jsondb import JSONDB

testdata = [
    {
        "one": 1,
        "two": 2,
        "three": 3
    },
    {
        "one": 1,
        "two": 3,
        "three": 2
    },
    {
        "one": 3,
        "two": 2,
        "three": 1
    }
]


def clean_data():
    if os.path.isfile(TEST_DATA_PATH):
        os.remove(TEST_DATA_PATH)
    with open(TEST_DATA_PATH, "w") as f:
        json.dump(testdata, f)


def test_creating_missing_file():
    missing_path = os.path.join(TEST_PATH, "missing.json")
    if os.path.isfile(missing_path):
        os.remove(missing_path)
    JSONDB(missing_path)
    assert os.path.isfile(missing_path)


def test_loading_file():
    clean_data()
    db = JSONDB(TEST_DATA_PATH)
    assert len(db) == 3


def test_select():
    clean_data()
    db = JSONDB(TEST_DATA_PATH)
    assert len(db.select(lambda x: x["one"] == 1)) == 2


def test_chained_select():
    clean_data()
    db = JSONDB(TEST_DATA_PATH)
    assert len(db.select(lambda x: x["one"] == 1).select(lambda x: x["two"] == 2)) == 1


def test_update_rows():
    clean_data()
    db = JSONDB(TEST_DATA_PATH)
    assert len(db.select(lambda x: x["two"] == 2)) == 2
    swapped_row = db.select(lambda x: x["two"] == 3)
    swapped_row.update("two", 2)
    assert len(db.select(lambda x: x["two"] == 2)) == 3
