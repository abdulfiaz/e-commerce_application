import base64
from adminapp.models import CustomUser, IUMaster, RoleMaster, UserRoleMapping,SellerRegistration
from adminapp.token import authorization
from e_commerce.settings import EMAIL_HOST_USER
import graphene
from graphene_django import DjangoObjectType
from graphene_django.views import GraphQLView
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import transaction

# used to get role name
def tokenRole_name(info):
    token_data=authorization(info)
    try:
        user_id=token_data.get('user_id')
    except Exception as e:
        raise Exception({"Token not provided"})
    user_data=UserRoleMapping.objects.get(user=user_id)
    role_name=user_data.role.role_name
    return role_name

class RoleType(DjangoObjectType):
    class Meta:
        model = RoleMaster

class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class IuIdType(DjangoObjectType):
    class Meta:
        model=IUMaster

class SellerregisterType(DjangoObjectType):
    class Meta:
        model=SellerRegistration

class Query(graphene.ObjectType):
    all_roles = graphene.List(RoleType)
    all_users = graphene.List(CustomUserType)
    all_iuId = graphene.List(IuIdType)
    all_registers=graphene.List(SellerregisterType,seller_status=graphene.String())

    def resolve_all_roles(self,info):
        role_name=tokenRole_name(info)
        if not role_name in ['manager']:
            raise Exception("unauthorized user")
        roles=RoleMaster.objects.all()
        return roles
        
    def resolve_all_users(self,info):
        role_name=tokenRole_name(info)
        if not role_name in ['manager']:
            raise Exception("unauthorized user")
        Users=CustomUser.objects.all()
        return Users
    
    def resolve_all_iuId(self,info):
        role_name=tokenRole_name(info)
        if not role_name in ['manager']:
            raise Exception("unauthorized user")
        iuid=IUMaster.objects.all()
        return iuid
    
    def resolve_all_registers(self,info,seller_status=None):
        role_name=tokenRole_name(info)
        if not role_name in ['manager']:
            raise Exception("unauthorized user")
        register=SellerRegistration.objects.all()
        if seller_status == 'pending':
            register = SellerRegistration.objects.filter(seller_status='pending')
            return register
        if seller_status == 'approved':
            register = SellerRegistration.objects.filter(seller_status='approved')
            return register
        if seller_status == 'rejected':
            register = SellerRegistration.objects.filter(seller_status='rejected')
            return register
        return register

    
class CreateUser(graphene.Mutation):
    class Arguments:
        first_name=graphene.String(required=True)
        last_name=graphene.String()
        email=graphene.String(required=True)
        password=graphene.String(required=True)
        mobile_number=graphene.Int(required=True)
        date_of_birth=graphene.String(required=True)
        # iu_id=graphene.Int(required=True)
        role_id=graphene.Int(required=True)
        gst_number=graphene.Int()
        business_name=graphene.String()

        
    user=graphene.Field(CustomUserType)

    def mutate(self,info,first_name,last_name,email,password,mobile_number,date_of_birth,role_id,gst_number,business_name):
        try:
            transaction.set_autocommit(False)
            token_data=authorization(info)
            try:
                user_id=token_data.get('user_id')
            except Exception as e:
                raise Exception({"no token provided"})
            user_data=UserRoleMapping.objects.get(user=user_id)
            role_name=user_data.role.role_name

            if not role_name in ['admin','manager']:
                transaction.rollback()
                raise Exception("unauthorized user")
            
            user_role=RoleMaster.objects.get(id=role_id)

            host = info.context.get_host()
            ium=IUMaster.objects.all()
            for iu in ium:
                if host in iu.host[0]:
                    IU_ID=iu
                    break 
            # IU_ID=IUMaster.objects.get(id=iu_id)
            users=CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=f"{first_name}.{last_name}",
                email=email,
                password=make_password(password),
                mobile_number=mobile_number,
                date_of_birth=date_of_birth,
                created_by=user_id,
                modified_by=user_id,
                iu_id=IU_ID
            )
            users.save()
            
            user_role_mapping=UserRoleMapping(
                user=users,
                role=user_role
            )
            user_role_mapping.save()
            
            if user_role.role_name in ['seller']:
                seller_registration=SellerRegistration(
                    user=users,
                    gst_no=gst_number,
                    bussiness_name=business_name,
                    created_by=user_id,
                    modified_by=user_id
                )
                seller_registration.save()


            subject='user registered successfully'
            message=f'your email : {email} \nyour password : {password}'
            abs_path=r"C:\Users\kingk\Downloads\welcome.jpg"
            try:
                with open(abs_path, 'rb') as img_file:
                    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
            except Exception as e:
                print(str(e))
                raise Exception(str(e))
        # Create the context for the email template
            context = {
                'email': email,
                'password': password,
                'encoded_image': encoded_image
            }
            html_message = render_to_string('template.html', context)
            send_mail(subject,message,EMAIL_HOST_USER,[email],html_message=html_message)
            transaction.commit()
            return CreateUser(user=users)
        except IUMaster.DoesNotExist:
            transaction.rollback()
            raise Exception("IU_ID does not exist")
        except RoleMaster.DoesNotExist:
            transaction.rollback()
            raise Exception("roleMaster does not exist")
        except Exception as e:
            transaction.rollback()
            raise Exception(str(e))
class Mutation(graphene.ObjectType):
    create_user=CreateUser.Field()

schema=graphene.Schema(query=Query,mutation=Mutation)

class GraphQLAPI(GraphQLView):
    schema = schema


