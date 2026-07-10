import requests
import json
import time
import random

# ---------------- CONFIG ---------------- #

URL = "https://wmsc.lcsc.com/ftps/wm/product/query/list"

# Replace with the LCSC category ID you want to scrape
CATEGORY_ID = 0

# 🔴 CHANGE RAW FILE NAME HERE
RAW_FILE = "lcsc_raw.jsonl"

# Replace with one or more LCSC brand IDs
BRAND_IDS = ["BRAND_ID_HERE"]


# ---------------- HEADERS ---------------- #

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.lcsc.com",
    "Referer": "https://www.lcsc.com/",
    "X-Requested-With": "XMLHttpRequest"
}

# ---------------- SESSION ---------------- #

session = requests.Session()
session.headers.update(HEADERS)

# Initialize session
session.get("https://www.lcsc.com/")

print("✅ Scraper started")

# ---------------- DELAY ---------------- #

def delay(page):

    r = random.random()

    if r < 0.6:
        d = random.uniform(3, 5)

    elif r < 0.85:
        d = random.uniform(5, 7)

    else:
        d = random.uniform(7, 12)

    # Progressive slowdown
    if page > 30:
        d += random.uniform(1, 2)

    if page > 50:
        d += random.uniform(2, 3)

    # Small random jitter
    return d + random.uniform(0.1, 0.9)


# ---------------- ATTRIBUTE EXTRACTION ---------------- #

def extract_all_attributes(params):

    data = {}

    for p in params:

        name = (
            p.get("paramNameEn")
            or p.get("paramName")
            or ""
        ).strip()

        val = (
            p.get("paramValueEn")
            or p.get("paramValue")
            or ""
        ).strip()

        if val and val != "-":
            data[name] = val

    return data


# ---------------- FETCH PAGE ---------------- #

def fetch_page(payload):

    for _ in range(5):

        try:

            res = session.post(
                URL,
                json=payload,
                timeout=15
            )

            if res.status_code == 200:

                data = res.json()

                if (
                    data
                    and data.get("result")
                    and data["result"].get("dataList") is not None
                ):
                    return data

            elif res.status_code == 429:

                wait = random.uniform(60, 120)

                print(
                    f"🚫 429 → sleep {wait:.1f}s"
                )

                time.sleep(wait)

        except Exception as e:

            print(f"❌ Error: {e}")

        # Retry delay
        time.sleep(
            random.uniform(2, 5)
        )

    return None


# ---------------- MAIN SCRAPING LOOP ---------------- #
failed_brands = []

for brand_id in BRAND_IDS:

    print(
        f"\n🔥 Scraping brand ID: {brand_id}"
    )

    page = 1
    fail_count = 0

    while True:

        print(
            f"\n🔄 Page {page}"
        )

        payload = {

            "keyword": "",

            "catalogIdList": [
                CATEGORY_ID
            ],

            "currentPage": page,

            "pageSize": 100,

            "brandIdList": [
                brand_id
            ]
        }

        data = fetch_page(payload)

        # ---------------- FAILED REQUEST ---------------- #

        if not data:

            fail_count += 1

            print(
                f"❌ Failed page ({fail_count})"
            )

            if fail_count >= 3:

                print(
                    "🛑 Ending this brand due to repeated failures"
                )

                failed_brands.append(brand_id)

                break

            continue

        else:

            fail_count = 0


        # ---------------- GET PRODUCTS ---------------- #

        products = (
            data
            .get("result", {})
            .get("dataList", [])
        )


        # ---------------- END OF BRAND ---------------- #

        if not products:

            print(
                "✅ Finished this brand"
            )

            break


        # ---------------- SAVE PRODUCTS ---------------- #

        with open(
            RAW_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            for item in products:

                attrs = extract_all_attributes(
                    item.get("paramVOList") or []
                )

                row = {

                    "Product Code":
                        item.get("productCode"),

                    "MPN":
                        item.get("productModel"),

                    "Description": (
                        item.get("productIntroEn")
                        or item.get("productDescEn")
                        or item.get("productDesc")
                        or ""
                    ),

                    "Package":
                        item.get("encapStandard"),

                    "Brand": (
                        item.get("brandNameEn")
                        or item.get("brandName")
                    ),

                    "Brand ID Used":
                        brand_id,

                    "attributes":
                        attrs
                }

                f.write(
                    json.dumps(
                        row,
                        ensure_ascii=False
                    )
                    + "\n"
                )


        print(
            f"💾 Saved page {page}"
        )


        # ---------------- DELAY ---------------- #

        sleep_time = delay(page)

        print(
            f"⏳ Sleep {sleep_time:.2f}s"
        )

        time.sleep(sleep_time)


        # Move to next page
        page += 1


if failed_brands:

    print(
        "\n⚠️ SCRAPING FINISHED WITH INCOMPLETE BRANDS"
    )

    print(
        f"Failed brand IDs: {failed_brands}"
    )

else:

    print(
        "\n🎉 ALL BRANDS SCRAPED SUCCESSFULLY"
    )