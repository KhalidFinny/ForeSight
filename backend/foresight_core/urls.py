from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from inventory.views import ProductViewSet, SalesRecordViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'sales', SalesRecordViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
