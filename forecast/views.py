from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .utils import predict_sales
from inventory.models import Product
from rest_framework.decorators import api_view
import os
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from inventory.models import SalesRecord

MODEL_DIR = "forecast/models"

class ForecastAPIView(APIView):
    def get(self, request, product_id):
        # Ambil tanggal dari query param
        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"error": "Missing 'date' query parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        prediksi = predict_sales(product_id, target_date)
        if prediksi is None:
            return Response({"error": "No model or sales data for this product"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"product_id": product_id, "date": date_str, "prediction": prediksi})

@api_view(["POST"])
def retrain_models(request):
    os.makedirs(MODEL_DIR, exist_ok=True)
    products = Product.objects.all()
    trained_products = []

    for product in products:
        qs = SalesRecord.objects.filter(product=product).order_by("sale_date")
        if not qs.exists():
            continue

        first_date = qs.first().sale_date
        X = np.array([(record.sale_date - first_date).days for record in qs]).reshape(-1, 1)
        y = np.array([record.quantity_sold for record in qs])

        model = LinearRegression()
        model.fit(X, y)

        model_path = os.path.join(MODEL_DIR, f"product_{product.id}.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        trained_products.append(product.name)

    return Response({"trained": trained_products, "status": "success"})
