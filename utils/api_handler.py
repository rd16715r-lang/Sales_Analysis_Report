import requests

BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
        print(f"Fetched {len(products)} products successfully")
        return products
    except requests.RequestException as e:
        print("Failed to fetch products:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product info
    Returns: dictionary
    """
    mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is None:
            continue

        mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
        }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches sales transactions with API product data
    Returns: list of enriched transactions
    """
    enriched_transactions = []

    for tx in transactions:
        tx_copy = tx.copy()

        api_category = None
        api_brand = None
        api_rating = None
        api_match = False

        try:
            product_id = tx.get("ProductID")
            api_id = int(product_id[1:]) % 100
            product_info = product_mapping.get(api_id)

            if product_info:
                api_category = product_info.get("category")
                api_brand = product_info.get("brand")
                api_rating = product_info.get("rating")
                api_match = True

        except Exception:
            api_match = False

        tx_copy["API_Category"] = api_category
        tx_copy["API_Brand"] = api_brand
        tx_copy["API_Rating"] = api_rating
        tx_copy["API_Match"] = api_match

        enriched_transactions.append(tx_copy)

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to pipe-delimited file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = []
            for h in headers:
                value = tx.get(h)
                row.append("" if value is None else str(value))
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
