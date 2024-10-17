from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Q


def api_response(success, message, data=None):
    """Utility function to standardize API responses."""
    return Response({
        "success": success,
        "message": message,
        "data": data,
    })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(category__name__icontains=search)
            )
        # Add an explicit ordering here, for example by 'id'
        return queryset.order_by('id')

    def create(self, request, *args, **kwargs):
        product_name = request.data.get('name')

        # Check if a product with the same name already exists
        if product_name and Product.objects.filter(name=product_name).exists():
            raise serializers.ValidationError(f"Product with name '{product_name}' already exists.")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(
                success=True,
                message="Product created successfully.",
                data=serializer.data
            )

        return api_response(
            success=False,
            message="Product creation failed.",
            data=serializer.errors
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)  
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # Return paginated response

        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            success=True,
            message="Products retrieved successfully.",
            data=serializer.data
        )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(
            success=True,
            message="Category retrieved successfully.",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return api_response(
                success=True,
                message="Product updated successfully.",
                data=serializer.data
            )
        return api_response(
            success=False,
            message="Product update failed.",
            data=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(
            success=True,
            message="Product deleted successfully."
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(
                success=True,
                message="Category created successfully.",
                data=serializer.data
            )
        return api_response(
            success=False,
            message="Category creation failed.",
            data=serializer.errors
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)  
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # Return paginated response

        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            success=True,
            message="Products retrieved successfully.",
            data=serializer.data
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(
            success=True,
            message="Category retrieved successfully.",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return api_response(
                success=True,
                message="Category updated successfully.",
                data=serializer.data
            )
        return api_response(
            success=False,
            message="Category update failed.",
            data=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(
            success=True,
            message="Category deleted successfully."
        )
