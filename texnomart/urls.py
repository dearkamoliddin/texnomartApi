from django.urls import path
from rest_framework.authtoken import views
from texnomart.views.auth import LoginAPIView, LogoutAPIView, RegisterAPIView
from texnomart.custom_token import CustomAuthToken
from texnomart.views.category import CategoryListView, CategoryAddView, CategoryUpdateView, CategoryDeleteView
from texnomart.views.product import (
    ProductListView,
    ProductAllView,
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
    path('product/detail/<int:id>/', ProductDetailView.as_view()),
    path('product/<int:id>/edit/', ProductUpdateView.as_view()),
    path('product/<int:id>/delete/', ProductDeleteView.as_view()),

    # attributes
    path('attributes/', ProductAttributeView.as_view()),
    path('attribute-key/', KeyView.as_view()),
    path('attribute-value/', ValueView.as_view()),


    path('api-token-auth/', CustomAuthToken.as_view()),

    # Login View
    path("login/", LoginAPIView.as_view(), name="user_login"),
    path("register/", RegisterAPIView().as_view(), name="user_register"),
    path("logout/", LogoutAPIView.as_view(), name="user_logout")

]
