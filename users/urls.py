from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static

from .views import CategoryView,SubCategoryView
urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryView.as_view(), name='category-detail'),
    path('product/',SubCategoryView.as_view(),name='products'),
    
]