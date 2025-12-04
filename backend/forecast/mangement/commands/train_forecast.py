from django.core.management.base import BaseCommand
from forecast.ml.trainer import train_model

class Command(BaseCommand):
    help = "Train the forecast linear regression model"

    def handle(self, *args, **kwargs):
        result = train_model()
        self.stdout.write(self.style.SUCCESS(result))
