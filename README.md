# LCSC Product Data Pipeline

A Python-based data pipeline for extracting electronic component product data from LCSC and transforming raw JSONL records into a structured CSV dataset.

## Overview

The project consists of two stages:

1. `scraper.py` retrieves paginated product data for a selected LCSC category and one or more brands.
2. `cleaner.py` converts the raw JSONL data into a structured CSV file.

The pipeline dynamically extracts technical product attributes and expands them into separate CSV columns.

## Pipeline

LCSC product data  
→ Category and brand filtering  
→ Paginated API requests  
→ Raw JSONL storage  
→ Dynamic attribute extraction  
→ Structured CSV output

## Features

- Category-based product extraction
- Multiple brand ID filtering
- Automatic pagination
- Automatic transition between brands
- Raw JSONL storage
- Dynamic technical attribute extraction
- Structured CSV generation
- Retry handling for failed requests
- Rate-limit handling for HTTP 429 responses
- Randomized request delays
- Incomplete-brand detection and reporting

## Project Structure

```text
lcsc-product-data-pipeline/
├── scraper.py
├── cleaner.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository and install the required dependency:
```bash
pip install -r requirements.txt
```
## Configuration
Before running the scraper, edit the configuration section in scraper.py:
```Python
CATEGORY_ID = 0

BRAND_IDS = [
    "BRAND_ID_HERE"
]

RAW_FILE = "lcsc_raw.jsonl"
```
Replace the placeholder values with the category and brand IDs you want to query.
## Usage
Run the scraper:
```bash
python scraper.py
```
The scraper writes raw product records to:
```text
lcsc_raw.jsonl
```
Then run the cleaner:
```bash
python cleaner.py
```
The cleaner generates:
```text
lcsc_clean.csv
```

## Output Data
The CSV contains fixed product fields such as:
- Product Code
- MPN
- Description
- Package
- Brand
- Brand ID Used
  
Technical product attributes are discovered dynamically from the raw data and added as additional CSV columns.

## Known Limitation
During testing, queries with more than 5,000 matching products could not continue beyond page 50 when using a page size of 100.

The scraper reports the affected brand as incomplete and continues processing the remaining configured brands.

Large result sets may therefore require additional query partitioning.

## Disclaimer
This project is intended for educational and portfolio purposes. Users are responsible for ensuring that their use of the code complies with the target website's terms, policies, and applicable requirements.


