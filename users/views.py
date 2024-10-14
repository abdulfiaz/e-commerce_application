from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from adminapp.models import UserRoleMapping
from .models import CategoryMaster,SubCategory
from rest_framework import status
from rest_framework.views import APIView
 
 
def check(user):
    user_id=user.id
    user_map= UserRoleMapping.objects.get(user=user_id)
    return user_map
 
class CategoryView(APIView):
    def post(self,request):
        try:
            if check(request.user).role.role_name in ['admin']:
                data=request.data
                category_name=data.get('category_name')
                if not category_name:
                    return Response({'error':'category name required'},status=status.HTTP_400_BAD_REQUEST)
                category=CategoryMaster.objects.create(caetgory_name=category_name)
                response_data={
                    'id':category.id,
                    'category_name':category.category_name,
                    'created_at':category.created_at,
                    'modified_at':category.modified_at,
                    'created_by':category.user.id,
                    'modified_by':category.user.id
                }
                return Response(response_data,status=status.HTTP_201_CREATED)
            else:
                return Response({'unauthorized user'},status=status.HTTP_401_UNAUTHORIZED)
        except CategoryMaster.DoesNotExists:
            return Response({'error':'Invalid'},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request):
        try:
            if check(request.user).role.role_name in ['admin']:
                data=request.data
                category_id=data.get('category_id')
                category_name=data.get('category_name')
                try:
                    categories=CategoryMaster.objects.get(id=category_id)
                except CategoryMaster.DoesNotExit:
                    return Response({'error':'category not found'},status=status.HTTP_404_NOT_FOUND)


                if categories:
                    categories.category_id=category_id
                    categories.category_name=category_name

                categories.save()
                
                response_data={
                    category_id=categories.category.id,
                    category_name=categories.category_name,
                    created_by=request.user,
                    modified_by=request.user,
                    modified_at=categories.modified_at
                }

                return Response({'data':response_data},status=status.HTTP_200_OK)   
            else:
                return Response({'unsuthorized'},status=status.HTTP_401_UNAUTHORIZED)
        except CategoryMaster.DoesNotExist:
            return Response({'error':'invalid'},status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):

        if check(request.user).role.role_name in ['admin']:
            try:
                data=request.data
                category_id=data.get(category_id)
                category = CategoryMaster.objects.get(id=category_id)
                category.is_active = False 
                category.save()
                return Response({'message': 'Category deleted'}, status=status.HTTP_204_NO_CONTENT)
            except CategoryMaster.DoesNotExist:  
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)



class SubCategoryView(APIView):
    def post(self,request):
        try:
            if check(request.user).role.role_name in ['admin,manager']:
                data=request.data
                category_id=data.get('category_id')
                product_name=data.get('product_name')
                price=data.get('price')
                quantity=data.get('quantity')
                if not category_id:
                    return Response({'error':'category id required'},status=status.HTTP_400_BAD_REQUEST)
                try:
                    products=CategoryMaster.objects.get(id=category_id)
                except CategoryMaster.DoesNotExist:
                    return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
                try:
                    user=SubCategory{
                        category=category_id,
                        product_name=products.product_name,
                        price=products.product_price,
                        quantity=products.quantity
                        }
                    user.save()
                    return Response({'product created successfully'},status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
            else:
                return Response({'unauthorized user'},status=status.HTTP_401_UNAUTHORIZED)
        except SubCategory.DoesNotExists:
            return Response({'error':'Invalid'},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request):
        try:
            if check(request.user).role.role_name in ['manager,admin']:
                data=request.data
                category_id=data.get('category_id')
                product_id=data.get("product_id")
                category_name=data.get('product_name')
                
                try:
                    products=SubCategory.objects.get(id=product_id)
                except SubCategory.DoesNotExit:
                    return Response({'error':'product not found'},status=status.HTTP_404_NOT_FOUND)


                if products:
                    products.product_id=product_id
                    products.product_name=product_name

                products.save()
                
                response_data={
                    products_id=products.product.id,
                    product_name=products.product_name,
                    created_by=request.user,
                    modified_by=request.user,
                    modified_at=products.modified_at
                }

                return Response({'data':response_data},status=status.HTTP_200_OK)   
            else:
                return Response({'unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
        except products.DoesNotExist:
            return Response({'error':'invalid'},status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):

        if check(request.user).role.role_name in ['admin']:
            try:
                data=request.data
                product_id=data.get(product_id)
                products = SubCategory.objects.get(id=product_id)
                products.is_active = False 
                products.save()
                return Response({'message': 'Category deleted'}, status=status.HTTP_204_NO_CONTENT)
            except SubCategory.DoesNotExist:  
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)