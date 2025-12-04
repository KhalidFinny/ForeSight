from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import SalesRecord
from .tasks import retrain_forecast

@receiver(post_save, sender=SalesRecord)
def retrain_on_new_sale(sender, instance, created, **kwargs):
    if created:
        retrain_forecast.delay()
