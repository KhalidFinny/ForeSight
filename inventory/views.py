from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from .models import Product, SalesRecord
from .serializers import ProductSerializer, SalesRecordSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock_quantity', 'created_at']

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        product = self.get_object()
        sales = SalesRecord.objects.filter(product=product)
        serializer = SalesRecordSerializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        product = self.get_object()
        amount = int(request.data.get('amount', 0))

        if amount <= 0:
            return Response({"error": "Amount must be > 0"}, status=400)

        product.stock_quantity += amount
        product.save()

        return Response({"message": "Stock updated", "new_stock": product.stock_quantity})

    def perform_create(self, serializer):
        sale = serializer.save()
        product = sale.product

        if product.stock_quantity < sale.quantity_sold:
            raise ValidationError("Insufficient stock")

        product.stock_quantity -= sale.quantity_sold
        product.save()

class SalesRecordViewSet(viewsets.ModelViewSet):
    queryset = SalesRecord.objects.all()
    serializer_class = SalesRecordSerializer
