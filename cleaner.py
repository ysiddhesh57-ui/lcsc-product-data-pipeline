import json
import csv

# ---------------- CONFIG ---------------- #

# 🔴 MUST MATCH THE SCRAPER RAW FILE NAME
RAW_FILE = "lcsc_raw.jsonl"

# 🔴 CHANGE OUTPUT FILE NAME HERE
OUTPUT_FILE = "lcsc_clean.csv"


# ---------------- LOAD RAW DATA ---------------- #

rows = []

all_attributes = set()


with open(
    RAW_FILE,
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        row = json.loads(line)

        rows.append(row)

        attributes = (
            row.get("attributes")
            or {}
        )

        all_attributes.update(
            attributes.keys()
        )


# ---------------- SORT ATTRIBUTE COLUMNS ---------------- #

attribute_columns = sorted(
    all_attributes
)


# ---------------- FIXED COLUMNS ---------------- #

fixed_columns = [

    "Product Code",

    "MPN",

    "Description",

    "Package",

    "Brand",

    "Brand ID Used"
]


# ---------------- ALL CSV COLUMNS ---------------- #

fieldnames = (
    fixed_columns
    + attribute_columns
)


# ---------------- WRITE CLEAN CSV ---------------- #

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()


    for row in rows:

        clean_row = {

            "Product Code":
                row.get("Product Code"),

            "MPN":
                row.get("MPN"),

            "Description":
                row.get("Description"),

            "Package":
                row.get("Package"),

            "Brand":
                row.get("Brand"),

            "Brand ID Used":
                row.get("Brand ID Used")
        }


        attributes = (
            row.get("attributes")
            or {}
        )


        for column in attribute_columns:

            clean_row[column] = (
                attributes.get(column, "")
            )


        writer.writerow(
            clean_row
        )


print(
    "🎉 CLEAN CSV GENERATED"
)