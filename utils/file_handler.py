def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()

            # remove header and empty lines
            cleaned = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    cleaned.append(line)

            return cleaned

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        if len(parts) != 8:
            continue

        try:
            transaction_id, date, product_id, product_name, qty, price, customer_id, region = parts

            product_name = product_name.replace(",", "")
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))

            transactions.append({
                "TransactionID": transaction_id,
                "Date": date,
                "ProductID": product_id,
                "ProductName": product_name,
                "Quantity": qty,
                "UnitPrice": price,
                "CustomerID": customer_id,
                "Region": region
            })

        except ValueError:
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    valid = []
    invalid_count = 0

    for tx in transactions:
        try:
            if (
                tx["Quantity"] <= 0 or
                tx["UnitPrice"] <= 0 or
                not tx["TransactionID"].startswith("T") or
                not tx["ProductID"].startswith("P") or
                not tx["CustomerID"].startswith("C")
            ):
                invalid_count += 1
                continue

            valid.append(tx)

        except KeyError:
            invalid_count += 1

    total_input = len(transactions)

    regions = sorted(set(tx["Region"] for tx in valid))
    print("Available Regions:", regions)

    amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in valid]
    if amounts:
        print("Transaction Amount Range:", min(amounts), "-", max(amounts))

    filtered_by_region = 0
    if region:
        before = len(valid)
        valid = [tx for tx in valid if tx["Region"] == region]
        filtered_by_region = before - len(valid)
        print("After region filter:", len(valid))

    filtered_by_amount = 0
    if min_amount is not None:
        before = len(valid)
        valid = [tx for tx in valid if tx["Quantity"] * tx["UnitPrice"] >= min_amount]
        filtered_by_amount += before - len(valid)

    if max_amount is not None:
        before = len(valid)
        valid = [tx for tx in valid if tx["Quantity"] * tx["UnitPrice"] <= max_amount]
        filtered_by_amount += before - len(valid)

    if min_amount or max_amount:
        print("After amount filter:", len(valid))

    summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid)
    }

    return valid, invalid_count, summary


