import csv
from pathlib import Path

from schemas.dataset import Dataset


"""
Loads a dataset from a CSV file and returns a Dataset object.
Also can use Pandas to load the dataset.

Args:
    path: The path to the CSV file.

Returns:
    A Dataset object.
"""


def load_dataset(path: Path) -> Dataset:
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        all_rows = list(reader)

    columns = all_rows[0] if all_rows else []

    rows = []
    for row in all_rows[1:]:
        row_dict = dict(zip(columns, row))
        rows.append(row_dict)

    return Dataset(rows=rows, columns=columns)
