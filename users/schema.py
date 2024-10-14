import graphene
from graphene_django import DjangoObjectType
from users.models import CategoryMaster
from graphene_django.views import GraphQLView

class category_type(DjangoObjectType):
    class Meta:
        model=CategoryMaster

class Query(graphene.objectype):
    all_category=graphene.List(category_type)
    def resolve_all_category(self,info):
        category=CategoryMaster.objects.all()
        return category
    
schema=graphene.schema(query=Query)

class GraphQLAPI(GraphQLView):
    schema=schema
          
