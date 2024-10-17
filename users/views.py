import re
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from adminapp.models import UserRoleMapping,SellerRegistration
from .models import CategoryMaster,SubCategory,Cart
from rest_framework.views import APIView,status
 
 
def check(user):
    user_id=user.id
    user_map= UserRoleMapping.objects.get(user=user_id)
    return user_map
 
class CategoryView(APIView):
    def post(self, request):
        try:
           
                # Ensure the user is authenticated and has the right role
            if check(request.user).role.role_name not in ['manager']:
                return Response({'error': 'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)

            # Extract category name from the request data
            data = request.data
            category_name = data.get('category_name')

            # Validate that the category name is provided and contains only letters and spaces
            if not category_name or not re.match(r'^[A-Za-z][A-Za-z\s]*$', category_name):
                return Response({'error': 'Category name should start with a letter and contain only letters and spaces'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a category with the same name already exists
            if CategoryMaster.objects.filter(category_name=category_name).exists():
                return Response({'error': 'Category with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the category
            category = CategoryMaster.objects.create(category_name=category_name)

            # Prepare and return response
            response_data = {
                'id': category.id,
                'category_name': category.category_name
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        try:
              # Ensure the user is authenticated and has the right role
            if check(request.user).role.role_name not in ['buyer']:
                return Response({'error': 'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)


            data = request.data
            category_id = data.get('category_id')
            category_name = data.get('category_name')

            # Validate that both category_id and category_name are provided
            if not category_id or not category_name:
                return Response({'error': 'Category ID and name are required'},status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the category to update
            try:
                category = CategoryMaster.objects.get(id=category_id)
            except CategoryMaster.DoesNotExist:
                return Response({'error': 'Category not found'},status=status.HTTP_404_NOT_FOUND)

            # Check for uniqueness of the new category name
            if CategoryMaster.objects.filter(category_name=category_name).exclude(id=category_id).exists():
                return Response({'error': 'Category with this name already exists'},status=status.HTTP_400_BAD_REQUEST)

            # Update category details
            category.category_name = category_name
            category.save()

            # Prepare and return response data
            response_data = {
                'category_id': category.id,
                'category_name': category.category_name,
                'modified_by': request.user.id,
                'modified_at': category.modified_at
            }
            return Response({'data': response_data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Ensure the user is authenticated and has the right role
        if check(request.user).role.role_name not in ['buyer']:
            return Response({'error': 'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)

        category_id = request.data.get('category_id')

        if not category_id:
            return Response({'error': 'Category ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = CategoryMaster.objects.get(id=category_id)
            category.is_active = False  # Soft delete
            category.save()
            return Response({'message': 'Category deleted'}, status=status.HTTP_204_NO_CONTENT)
        except CategoryMaster.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

class SubCategoryView(APIView):
    def post(self, request):
        try:
            # Check if the user is a seller and their status is 'approved', or if they are a manager
            try:
                seller_registration = SellerRegistration.objects.get(user=request.user)
                
                # Check if the user is a seller with status 'approved'
                if seller_registration.seller_status != 'approved':
                    return Response({'error': 'Unauthorized user: seller status not approved'}, status=status.HTTP_401_UNAUTHORIZED)

            except SellerRegistration.DoesNotExist:
                # If the user is not a seller, check if they are a manager
                if request.user.role.role_name != 'manager':
                    return Response({'error': 'Unauthorized user: not a seller or manager'}, status=status.HTTP_401_UNAUTHORIZED)


            data = request.data
            category_id = data.get('category_id')
            product_name = data.get('product_name')
            price = data.get('price')
            quantity = data.get('quantity')

            # Validate required fields
            if not category_id or not product_name or price is None or quantity is None:
                return Response({'error': 'Category ID, product name, price, and quantity are required'},status=status.HTTP_400_BAD_REQUEST)

            # Check if the associated category exists
            try:
                category = CategoryMaster.objects.get(id=category_id)
            except CategoryMaster.DoesNotExist:
                return Response({'error': 'Category not found'},status=status.HTTP_404_NOT_FOUND)

            # Check for uniqueness of the product name
            if SubCategory.objects.filter(product_name=product_name).exists():
                return Response({'error': 'Product name must be unique'},status=status.HTTP_400_BAD_REQUEST)

            # Validate that price and quantity are positive
            if int(price) <= 0 or int(quantity) <= 0:
                return Response({'error': 'Price and quantity must be positive values'},status=status.HTTP_400_BAD_REQUEST)

            # Create the new product
            product = SubCategory(
                categroy=category,
                product_name=product_name,
                price=price,
                quantity=quantity
            )
            product.save()

            return Response({'message': 'Product created successfully'},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            # Check if the user is a seller and their status is 'approved', or if they are a manager
            try:
                seller_registration = SellerRegistration.objects.get(user=request.user)
                
                # Check if the user is a seller with status 'approved'
                if seller_registration.seller_status != 'approved':
                    return Response({'error': 'Unauthorized user: seller status not approved'}, status=status.HTTP_401_UNAUTHORIZED)

            except SellerRegistration.DoesNotExist:
                # If the user is not a seller, check if they are a manager
                if request.user.role.role_name != 'manager':
                    return Response({'error': 'Unauthorized user: not a seller or manager'}, status=status.HTTP_401_UNAUTHORIZED)


            data = request.data
            product_id = data.get("product_id")
            category_id = data.get("category_id")
            product_name = data.get('product_name')
            price = data.get('price')
            quantity = data.get('quantity')

            # Check for the existence of the product
            try:
                product = SubCategory.objects.get(id=product_id)
            except SubCategory.DoesNotExist:
                return Response({'error': 'Product not found'},status=status.HTTP_404_NOT_FOUND)

            # Validate that the updated name is unique
            if SubCategory.objects.filter(product_name=product_name).exclude(id=product_id).exists():
                return Response({'error': 'Product name must be unique'},status=status.HTTP_400_BAD_REQUEST)

            # Check if the category exists
            if category_id:
                try:
                    category = SubCategory.objects.get(id=category_id)
                except SubCategory.DoesNotExist:
                    return Response({'error': 'Category not found'},status=status.HTTP_404_NOT_FOUND)
                product.category = category  # Update the category if it exists

            # Validate price and quantity
            if price is not None and price <= 0:
                return Response({'error': 'Price must be a positive value'},status=status.HTTP_400_BAD_REQUEST)

            if quantity is not None and quantity < 0:
                return Response({'error': 'Quantity cannot be negative'},status=status.HTTP_400_BAD_REQUEST)

            # Update product fields
            product.product_name = product_name
            if price is not None:
                product.price = price
            if quantity is not None:
                product.quantity = quantity

            product.save()

            # Prepare the response data
            response_data = {
                'product_id': product.id,
                'product_name': product.product_name,
                'category_id': product.category.id if product.category else None,
                'price': product.price,
                'quantity': product.quantity,
                'modified_by': request.user.id,
                'modified_at': product.modified_at
            }

            return Response({'data': response_data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
    # Check if the user is a seller and their status is 'approved', or if they are a manager
        try:
            seller_registration = SellerRegistration.objects.get(user=request.user)
            
            # Check if the user is a seller with status 'approved'
            if seller_registration.seller_status != 'approved':
                return Response({'error': 'Unauthorized user: seller status not approved'}, status=status.HTTP_401_UNAUTHORIZED)

        except SellerRegistration.DoesNotExist:
            # If the user is not a seller, check if they are a manager
            if request.user.role.role_name != 'manager':
                return Response({'error': 'Unauthorized user: not a seller or manager'}, status=status.HTTP_401_UNAUTHORIZED)


        data = request.data
        product_id = data.get('product_id')  # Ensure this is properly referenced as a string

        # Attempt to deactivate the product
        try:
            product = SubCategory.objects.get(id=product_id)
            product.is_active = False
            product.save()
            return Response({'message': 'Product deleted successfully'},status=status.HTTP_204_NO_CONTENT)

        except SubCategory.DoesNotExist:
            return Response({'error': 'Product not found'},status=status.HTTP_404_NOT_FOUND)


class AddToCartView(APIView):
    def post(self, request):
        try:
        
            if check(request.user).role.role_name not in ['buyer']:
                return Response({'error': 'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)

            # Get the product ID, quantity, and action ('add_to_cart' or 'buy_now')
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))  # Default to 1 if not provided

            # Check if the product exists
            product = SubCategory.objects.get(id=product_id)

            # Add to Cart: The product is added to the cart whether it's "Buy Now" or "Add to Cart"
            cart_item, item_created = Cart.objects.get_or_create(user=request.user, product=product)
            if not item_created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity

            # Save the cart item
            cart_item.save()

            # # For 'Add to Cart', just return the cart details 
            # total_price = cart_item.quantity * product.price #seperate pro total
            # cart_items = Cart.objects.filter(user=request.user, is_active=True)
            # cart_total = sum(item.quantity * item.product.price for item in cart_items)
            # total_items_count = sum(item.quantity for item in cart_items)

            return Response({
                'message': 'Product added to cart successfully',
                'product_id': product.id,
                'quantity': cart_item.quantity
            }, status=status.HTTP_201_CREATED)

        except SubCategory.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self,request):
        try:
             
            if check(request.user).role.role_name not in ['buyer']:
                return Response({'error': 'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)
            
            data = request.data
            product_id = data.get("product_id")
            quantity=data.get("quantity")

            if not product_id and quantity:
                return Response({'error':'product_id and quantity is must to provide'},status=status.HTTP_404_NOT_FOUND)

            # Check for the existence of the product
            try:
                small_cart= Cart.objects.get(id=product_id)
            except Cart.DoesNotExist:
                return Response({'error': 'Product not found'},status=status.HTTP_404_NOT_FOUND)

            small_cart.product_id=product_id
            small_cart.quantity+=quantity
            small_cart.price=small_cart.product.price*quantity
            small_cart.save()

            response_data={
                'product_id':product_id,
                'quantity':quantity
            }
            return Response({'updated successfully'},status=status.HTTP_200_OK)
        
        except SubCategory.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            



