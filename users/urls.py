from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static
from users.schema import GraphQLAPI
from users.views import CategoryView,SubCategoryView,AddToCartView

urlpatterns = [
    path('categories/',CategoryView.as_view(), name='category-list'),
    path('graphql/', GraphQLAPI.as_view(graphiql=True)),
    path('product/',SubCategoryView.as_view(),name='products'),
    path('cart/add/',AddToCartView.as_view(), name='add-to-cart'),  # URL for adding products to cart
]
    
