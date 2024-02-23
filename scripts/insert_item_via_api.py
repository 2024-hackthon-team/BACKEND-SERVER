"""
使用例:
$ python scripts/insert_item_via_api.py "./hacku_item - シート1.csv"
"""

import csv
import sys
import typing as T
from pathlib import Path

import requests


def insert_item_by_api(host: str, data: dict):
    """
    POST /item

    {
        "item_name": "string",
        "product_label": "string",
        "img_url": "string",
        "item_tags": []
    }
    """
    url = f"{host.rstrip('/')}/item"
    response = requests.post(url, json=data)
    if not response.ok:
        print(response.text)
        print(f"Failed to insert {data}")


def convert_csv_to_dict(file_path: str) -> T.Generator[dict, None, None]:
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # pick item_name, product_label, its values are not empty
            if not all(row.get(key) for key in ["item_name", "product_label"]):
                print(f"Skipped: {row}")
                continue
            yield {
                "item_name": row["item_name"],
                "product_label": row["product_label"],
                "img_url": row["img_url"],
                "item_tags": (
                    row["item_tag"].split(",") if row.get("item_tag") else []
                ),
            }


if __name__ == "__main__":
    file_path = Path(sys.argv[1])
    url = "http://localhost:8000/"

    for data in convert_csv_to_dict(file_path):
        insert_item_by_api(url, data)
