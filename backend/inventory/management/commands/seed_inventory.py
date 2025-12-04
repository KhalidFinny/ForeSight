from django.core.management.base import BaseCommand
from inventory.models import Product, SalesRecord
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Seed initial inventory and sales data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding inventory data...")

        Product.objects.all().delete()
        SalesRecord.objects.all().delete()

        products_seed = [
            {
                "name": "Lenovo ThinkPad X1 Carbon",
                "description": "Premium business ultrabook",
                "stock_quantity": 35,
                "price": 23000000
            },
            {
                "name": "Logitech MX Master 3S",
                "description": "High-end productivity wireless mouse",
                "stock_quantity": 120,
                "price": 1500000
            },
            {
                "name": "Dell Ultrasharp 27 Monitor",
                "description": "Professional-grade color-accurate monitor",
                "stock_quantity": 15,
                "price": 5800000
            },
            {
                "name": "Kingston NVMe 1TB SSD",
                "description": "High-speed storage upgrade",
                "stock_quantity": 50,
                "price": 1350000
            },
            {
                "name": "HP LaserJet Pro M404dn",
                "description": "Business-grade laser printer",
                "stock_quantity": 10,
                "price": 4200000
            },
        ]

        created_products = []

        for item in products_seed:
            p = Product.objects.create(
                name=item["name"],
                description=item["description"],
                stock_quantity=item["stock_quantity"],
                price=item["price"],
            )
            created_products.append(p)

        self.stdout.write("Products created.")

        self.stdout.write("Creating sales records...")

        for product in created_products:
            # Generate 10 sales entries for each product
            for _ in range(10):
                SalesRecord.objects.create(
                    product=product,
                    quantity_sold=random.randint(1, 8),
                    sale_date=timezone.now() - timezone.timedelta(days=random.randint(1, 120))
                )

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
