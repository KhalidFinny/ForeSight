dates = [date(2025, 12, 5), date(2025, 12, 6), date(2025, 12, 7)]
for d in dates:
    print(f"{d}: {predict_sales(product_id, d)} pcs")
