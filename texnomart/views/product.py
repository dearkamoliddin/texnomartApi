import django_filters
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from texnomart.models import CategoryModel, ProductModel, AttributeModel, KeyModel, ValueModel
from texnomart.serializers import ProductSerializer, ProductModelSerializer, AttributeSerializer, KeySerializer, ValueSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache


class ProductPagination(PageNumberPagination):
    page_size = 10


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = ProductModel
        fields = ['name', 'category']


class ProductListView(ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'category__name']
    ordering_fields = '__all__'
    ordering = ['name']

    # def get_queryset(self):
    #     category_slug = self.kwargs.get('category_slug')
    #     if not category_slug:
    #         raise NotFound("Category slug not provided")
    #     category = get_object_or_404(CategoryModel, slug=category_slug)
    #     queryset = ProductModel.objects.filter(category=category).select_related('category')
    #     return queryset

    def get_queryset(self):
        queryset = ProductModel.objects.all()
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)

        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)

        return queryset


class ProductDetailView(RetrieveAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return ProductModel.objects.select_related('category').all()


class ProductUpdateView(RetrieveUpdateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = 'id'


class ProductDeleteView(RetrieveDestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = 'id'


class ProductAttributeView(ListCreateAPIView):
    queryset = AttributeModel.objects.all()
    #queryset = ProductModel.objects.select_related('group').prefetch_related('attributes__key', 'attributes__value')
    serializer_class = AttributeSerializer
    lookup_field = 'slug'


class KeyView(ListCreateAPIView):
    queryset = KeyModel.objects.all()
    serializer_class = KeySerializer


class ValueView(ListCreateAPIView):
    queryset = ValueModel.objects.all()
    serializer_class = ValueSerializer
