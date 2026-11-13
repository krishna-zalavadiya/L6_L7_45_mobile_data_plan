import math

def parse_plan(text):
    if not isinstance(text, str) or ':' not in text:
        return ("Unknown", 0.0)
    parts = text.split(':')
    if len(parts) != 2:
        return ("Unknown", 0.0)
    plan, gb_str = parts[0].strip(), parts[1].strip()
    if not plan:
        plan = "Unknown"
    try:
        gb = float(gb_str)
        if math.isnan(gb) or math.isinf(gb) or gb < 0:
            gb = 0.0
    except ValueError:
        gb = 0.0
    return plan.title(), gb

def usage_average(usage_csv):
    if not isinstance(usage_csv, str) or not usage_csv.strip():
        return 0
    values = []
    for item in usage_csv.split(','):
        item = item.strip()
        if not item:
            continue
        try:
            val = int(item)
            if val >= 0:
                values.append(val)
        except ValueError:
            continue
    if not values:
        return 0
    return sum(values) // len(values)

def payable_bill(text):
    if not isinstance(text, str) or '|' not in text:
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    try:
        bill = float(parts[0].strip())
        discount = float(parts[1].strip())
        if math.isnan(bill) or math.isinf(bill) or bill < 0:
            return 0.0
        if math.isnan(discount) or math.isinf(discount) or discount < 0:
            discount = 0.0
    except ValueError:
        return 0.0
    total = bill * 1.18 - discount
    return round(max(total, 0.0), 2)

def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter plan:data in GB (e.g. standard:5): ")
    result = parse_plan(user_input)
    print("Plan and Data:", result)

    print("\n==== Running usage_average ====")
    user_input = input("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    result = usage_average(user_input)
    print("Average Usage:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 399|50): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)

if __name__ == "__main__":
    main()