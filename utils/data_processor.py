from collections import defaultdict
from datetime import datetime


def calculate_total_revenue(transactions):
    total = 0.0
    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]
    return round(total, 2)


def region_wise_sales(transactions):
    region_data = defaultdict(lambda: {"total_sales": 0.0, "transaction_count": 0})

    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    result = {}
    for region, data in region_data.items():
        percentage = (data["total_sales"] / total_revenue) * 100 if total_revenue else 0
        result[region] = {
            "total_sales": round(data["total_sales"], 2),
            "transaction_count": data["transaction_count"],
            "percentage": round(percentage, 2),
        }

    return dict(
        sorted(result.items(), key=lambda x: x[1]["total_sales"], reverse=True)
    )


def top_selling_products(transactions, n=5):
    product_data = defaultdict(lambda: {"qty": 0, "revenue": 0.0})

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        product_data[name]["qty"] += qty
        product_data[name]["revenue"] += revenue

    products = [
        (name, data["qty"], round(data["revenue"], 2))
        for name, data in product_data.items()
    ]

    products.sort(key=lambda x: x[1], reverse=True)
    return products[:n]


def customer_analysis(transactions):
    customer_data = defaultdict(
        lambda: {"total_spent": 0.0, "purchase_count": 0, "products": set()}
    )

    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        customer_data[cid]["total_spent"] += amount
        customer_data[cid]["purchase_count"] += 1
        customer_data[cid]["products"].add(tx["ProductName"])

    result = {}
    for cid, data in customer_data.items():
        avg = (
            data["total_spent"] / data["purchase_count"]
            if data["purchase_count"]
            else 0
        )
        result[cid] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg, 2),
            "products_bought": sorted(list(data["products"])),
        }

    return dict(
        sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True)
    )


def daily_sales_trend(transactions):
    daily_data = defaultdict(
        lambda: {"revenue": 0.0, "transaction_count": 0, "customers": set()}
    )

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(tx["CustomerID"])

    result = {}
    for date, data in daily_data.items():
        result[date] = {
            "revenue": round(data["revenue"], 2),
            "transaction_count": data["transaction_count"],
            "unique_customers": len(data["customers"]),
        }

    return dict(sorted(result.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")))


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = max(daily.items(), key=lambda x: x[1]["revenue"])
    return (
        peak_date[0],
        peak_date[1]["revenue"],
        peak_date[1]["transaction_count"],
    )


def low_performing_products(transactions, threshold=10):
    product_data = defaultdict(lambda: {"qty": 0, "revenue": 0.0})

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        product_data[name]["qty"] += qty
        product_data[name]["revenue"] += revenue

    low_products = [
        (name, data["qty"], round(data["revenue"], 2))
        for name, data in product_data.items()
        if data["qty"] < threshold
    ]

    low_products.sort(key=lambda x: x[1])
    return low_products
