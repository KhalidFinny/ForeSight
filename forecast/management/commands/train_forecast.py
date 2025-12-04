# forecast/management/commands/train_forecast.py
import os
import pickle
from django.core.management.base import BaseCommand
from inventory.models import Product, SalesRecord
from sklearn.linear_model import LinearRegression
import numpy as np

class Command(BaseCommand):
    help = "Train Linear Regression model for sales forecast per product"

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            self.train_product(product)

    def handle_single_product(self, product):
        self.train_product(product)

    def train_product(self, product):
        from inventory.models import SalesRecord
        import os, pickle, numpy as np
        from sklearn.linear_model import LinearRegression

        qs = SalesRecord.objects.filter(product=product).order_by("sale_date")
        if not qs.exists():
            return

        first_date = qs.first().sale_date
        X = np.array([(r.sale_date - first_date).days for r in qs]).reshape(-1, 1)
        y = np.array([r.quantity_sold for r in qs])

        model = LinearRegression()
        model.fit(X, y)

        model_dir = "forecast/models"
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, f"product_{product.id}.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

            self.stdout.write(self.style.SUCCESS(
                f"Trained model for {product.name} -> saved as {model_path}"
            ))

        self.stdout.write(self.style.SUCCESS("All models trained successfully."))
