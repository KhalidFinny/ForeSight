from django.urls import path
from .views import ForecastAPIView, retrain_models

urlpatterns = [
    path('<int:product_id>/', ForecastAPIView.as_view(), name='forecast-product'),
    path('retrain/', retrain_models, name='forecast-retrain'),
]
