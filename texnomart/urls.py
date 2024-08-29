from django.urls import path
from rest_framework.authtoken import views
from texnomart.views.auth import LoginAPIView, LogoutAPIView, RegisterAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from texnomart.custom_obtain_view import CustomTokenObtainPairView, CustomTokenAuth
from texnomart.views.category import CategoryListView, CategoryAddView, CategoryUpdateView, CategoryDeleteView
from texnomart.views.product import (
    ProductListView,
    ProductAllView,
    ProductAddView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    ProductAttributeView,
    KeyView,
    ValueView,
)

urlpatterns = [
    # categories
    path('categories/', CategoryListView.as_view()),

    path('category/add-category/', CategoryAddView.as_view()),
    path('category/<slug:category_slug>/edit/', CategoryUpdateView.as_view()),
    path('category/<slug:category_slug>/delete/', CategoryDeleteView.as_view()),
    path('category/<slug:category_slug>/', ProductListView.as_view()),

    # products
    path('', ProductAllView.as_view()),
    path('product/add-product/', ProductAddView.as_view()),
    path('product/detail/<int:id>/', ProductDetailView.as_view()),
    path('product/<int:id>/edit/', ProductUpdateView.as_view()),
    path('product/<int:id>/delete/', ProductDeleteView.as_view()),

    # attributes
    path('attributes/', ProductAttributeView.as_view()),
    path('attribute-key/', KeyView.as_view()),
    path('attribute-value/', ValueView.as_view()),


    path('token-auth/', CustomTokenAuth.as_view()),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),

    # Login View
    path("login/", LoginAPIView.as_view(), name="user_login"),
    path("register/", RegisterAPIView().as_view(), name="user_register"),
    path("logout/", LogoutAPIView.as_view(), name="user_logout")

]
