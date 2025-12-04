import pickle
import os
from datetime import datetime

MODEL_DIR = "forecast/models"

def predict_sales(product_id, target_date):
    model_path = os.path.join(MODEL_DIR, f"product_{product_id}.pkl")
    if not os.path.exists(model_path):
        return None

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Hitung index hari dari tanggal pertama penjualan
    from inventory.models import SalesRecord
    qs = SalesRecord.objects.filter(product_id=product_id).order_by("sale_date")
    if not qs.exists():
        return None

    first_date = qs.first().sale_date
    day_index = (target_date - first_date).days
    prediction = model.predict([[day_index]])[0]
    return max(0, round(prediction))  # prediksi minimal 0
