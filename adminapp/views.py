import random
from django.shortcuts import render
from adminapp.models import CustomUser, IUMaster, RoleMaster, UserRoleMapping
from rest_framework.views import APIView,status
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from e_commerce.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail


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

