import django_filters
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from texnomart.models import CategoryModel, ProductModel
from texnomart.serializers import CategorySerializer
from texnomart import permissions
from django.core.cache import cache
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count


class CategoryPagination(PageNumberPagination):
    page_size = 10


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CategoryModel
        fields = ['title']


class CategoryListView(ListAPIView):
    # permission_classes = [permissions.CustomPermission]
    queryset = CategoryModel.objects.annotate(product_count=Count('product'))
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CategoryFilter
    search_fields = ['title']
    ordering_fields = '__all__'
    ordering = ['title']
    pagination_class = CategoryPagination

    def get_queryset(self):
        cache_key = 'category_list_' + str(self.request.query_params)
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        queryset = super().get_queryset()
        cache.set(cache_key, queryset, timeout=60 * 15)
        return queryset


class CategoryAddView(CreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateView(UpdateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(CategoryModel, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(CategoryModel, slug=slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(DestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(CategoryModel, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        category = get_object_or_404(CategoryModel, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
