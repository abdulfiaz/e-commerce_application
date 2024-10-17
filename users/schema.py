import graphene
from graphene_django import DjangoObjectType
from users.models import CategoryMaster,SubCategory
from graphene_django.views import GraphQLView

class category_type(DjangoObjectType):
    class Meta:
        model=CategoryMaster

class product_type(DjangoObjectType):
    class Meta:
        model=SubCategory

class Query(graphene.ObjectType):
    all_category=graphene.List(category_type)
    all_proucts=graphene.List(product_type)

    def resolve_all_category(self,info):
        category=CategoryMaster.objects.all()
        return category
    
    def resolve_all_products(self,info):
        products=SubCategory.objects.all()
        return products
    
schema=graphene.Schema(query=Query)

class GraphQLAPI(GraphQLView):
    schema=schema