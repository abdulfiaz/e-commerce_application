import random
from django.shortcuts import render
from adminapp.models import CustomUser, IUMaster, RoleMaster, SellerRegistration, UserRoleMapping
from rest_framework.views import APIView,status
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password,make_password
from e_commerce.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.timezone import now
from django.db import transaction


class RoleMaster_API(APIView):
    def post(self,request):
        try:
            user_id=request.user.id
            if not user_id:
                return Response({"status":"failed","message":"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
            user_role=UserRoleMapping.objects.get(user=user_id)

            if not user_role.role.role_name in ['admin']:
                return Response({"status":"failed","message":"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
        
            roleName=request.data.get("role_name")
            roleDescription=request.data.get("role_description")
            createdBy=request.user.id
            modifiedBy=request.user.id

            role=RoleMaster(
                role_name=roleName,
                role_description=roleDescription,
                created_by=createdBy,
                modified_by=modifiedBy
                )
            role.save()
            return Response({"status":"success","message":"Role inserted successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        try:
            role_id=request.data.get("role_id")
            role=RoleMaster.objects.get(id=role_id)
            role.role_name=("role_name",role.role_name)
            role.role_description=("role_description",role.role_description)
            role.save()
            return Response({"status":"success","message":"role data updated successfully"},status=status.HTTP_200_OK)
        except RoleMaster.DoesNotExist:
            return Response({"status":"failed","message":"role id does not exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            role_id=request.data.get("role_id")
            role=RoleMaster.objects.get(id=role_id)
            role.is_active=False
            role.save()
            return Response({"status":"success","message":"role successfully deleted"},status=status.HTTP_200_OK)
        except RoleMaster.DoesNotExist:
            return Response({"status":"failed","message":"role id does not exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

class IUMaster_API(APIView):
    def post(self,request):
        try:
            name=request.data.get("name")
            description=request.data.get("description")
            host=request.data.get("host")
            created_by=request.data.get("created_by")
            modified_by=request.data.get("modified_by")

            iu_master=IUMaster(
                host_name=name,
                description=description,
                host=host,
                created_by=created_by,
                modified_by=modified_by
            )
            iu_master.save()
            return Response({"status":"success","message":"iumaster created successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            iu_id=request.data.get("iu_id")
            iu_master=IUMaster.objects.get(id=iu_id)
            iu_master.is_active=False
            iu_master.save()
            return Response({"status":"success","message":"iuid deleted successfully"},status=status.HTTP_200_OK)
        except IUMaster.DoesNotExist:
            return Response({"status":"failed","message":"IUMaster id does not exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

class User_Role_Mapping_API(APIView):
    def post(self,request):
        try:
            user_id=request.data.get("user_id")
            role_id=request.data.get("role_id")

            user=CustomUser.objects.get(id=user_id)
            role=RoleMaster.objects.get(id=role_id)
            
            user_roles=UserRoleMapping.objects.get(user=user_id,role=role_id)
            if user_roles:
                return Response({"status":"failed","message":"same user is mapped for same role already"},status=status.HTTP_400_BAD_REQUEST)
            
            user_role_map=UserRoleMapping(
                user=user,
                role=role
            )
            user_role_map.save()
            return Response({"status":"sucess","message":"user manager mapped"})
        except CustomUser.DoesNotExist:
            return Response({"status":"failed","message":"user id does not exist"},status=status.HTTP_404_NOT_FOUND)
        except RoleMaster.DoesNotExist:
            return Response({"status":"failed","message":"role id does not exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
class LogInAPI(APIView):   
    def post(self,request):
        try:
            mobile_number=request.data.get("mobile_number")
            password=request.data.get("password")
            user=CustomUser.objects.get(mobile_number=mobile_number)
            if check_password(password,user.password):
                token=RefreshToken.for_user(user)
                access_token=str(token.access_token)
                return Response({"status":"success","message":access_token})
            else:
                return Response({"status":"failed","message":"invalid credentials"})
        except CustomUser.DoesNotExist:
            return Response({"status":"failed","message":"mobile number does not exist"})
        except Exception as e:
            return Response({"status":"error","message":str(e)})

class Forgot_passwordAPI(APIView):
    def post(self,request):
        try:
            transaction.set_autocommit(False)
            mobile_num=request.data.get('mobile_number')
            user=CustomUser.objects.get(mobile_number=mobile_num)
            otp = random.randint(111111,999999)
            email=user.email
            subject="forgot password"
            message=f"yor otp is : {otp}"
            user.temp_otp=otp
            send_mail(subject,message,EMAIL_HOST_USER,[email])
            user.save()
            transaction.commit()
            return Response({"status":"success","message":"otp sent successfully"},status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"status":"failed","message":"user does not exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.rollback()
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        try:
            transaction.set_autocommit(False)
            mobile_num=request.data.get('mobile_number')
            new_password=request.data.get('new_password')
            otp=request.data.get('otp')
            user=CustomUser.objects.get(mobile_number=mobile_num)
            if not (otp==user.temp_otp):
                return Response({"status":"failed","message":"invalid otp"},status=status.HTTP_400_BAD_REQUEST)
            user.password=make_password(new_password)
            email=user.email
            subject="forgot password"
            message=f"yor new_password is : {new_password}"
            send_mail(subject,message,EMAIL_HOST_USER,[email])
            user.save()
            transaction.commit()
            return Response({"status":"success","message":"password resetted successfully"},status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"status":"failed","message":"user does not exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class SellerRegisterApi(APIView):
    def post(self,request):
        user_id=request.user.id

        gst_no=request.data.get('gst_no')
        business_name=request.data.get('business_name')
        seller_status=request.data.get('seller_status')
        rejection_detail=request.data.get('rejection_detail')
        created_by=request.user.id
        modified_by=request.user.id
        


    def put(self,request):
        if not request.user.role.role_name in ['manager']:
            return Response({"status":"failed","message":"unauthorized access"},status=status.HTTP_401_UNAUTHORIZED)
        try:
            transaction.set_autocommit(False)
            sellerregistration_id=request.data.get("sellerregistration_id")
            seller_register=SellerRegistration.objects.get(id=sellerregistration_id)
            seller_register.seller_status=("status",seller_register.seller_status)
            
            if seller_register.seller_status in ['rejected']:
                reject_detail=request.data.get("rejection_detail")
                seller_register.rejection_detail=reject_detail
            
            seller_register.save()
            
            subject="Status of seller request"
            message=f"your request is {seller_register.seller_status}"
            send_mail(subject,message,EMAIL_HOST_USER,[seller_register.user.email])
            transaction.commit()
            return Response({"status":"success","message":"seller status updated successfully"},status=status.HTTP_200_OK)
        except SellerRegistration.DoesNotExist:
            return Response({"status":"failed","message":"registration id does not exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
            
class RoleSwitchingApi(APIView):
    def post(self,request):
        try:
            user_role=request.data.get("role")
            role=RoleMaster.objects.get(role_name=user_role)
            user=CustomUser.objects.get(id=request.user.id)
            # if user.last_login_role:
            #     if not user.last_login_role == user_role:
            #         return Response({"status":"failed","message":"only access through existing role"},status=status.HTTP_400_BAD_REQUEST)
            userroles=UserRoleMapping.objects.filter(user=user.id)
            for roles in userroles:
                if roles.role.role_name == role.role_name:
                    token=RefreshToken.for_user(user)
                    token['role_id']=role.id
                    token['role_name']=role.role_name   
                    # print(token['role_name']) 
                    # print(token['role_id'])            
                    access_token=str(token.access_token)
                    user.last_login_role=role.id
                    user.last_login=now()
                    user.save()
                    return Response({"status":"success","message":access_token},status=status.HTTP_200_OK)
            else:
                return Response({"status":"failed","message":"you are not elligible for that role"},status=status.HTTP_400_BAD_REQUEST)                
        except RoleMaster.DoesNotExist:
            return Response({"status":"failed","message":"Role does not exist"},status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"status":"failed","message":"mobile number does not exist"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

