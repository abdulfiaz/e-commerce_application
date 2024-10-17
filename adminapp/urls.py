from django.urls import path
from adminapp.views import RoleMaster_API,IUMaster_API,User_Role_Mapping_API,LogInAPI,Forgot_passwordAPI,RoleSwitchingApi,SubcategoryApi,SellerRegisterApi
from adminapp.schema import GraphQLAPI
urlpatterns=[
   path('graphql/', GraphQLAPI.as_view(graphiql=True)),

   path('rolemaster/',RoleMaster_API.as_view()),
   path('iuMaster/',IUMaster_API.as_view()),
   path('user_role/',User_Role_Mapping_API.as_view()),
   path('sign_in/',LogInAPI.as_view()),
   path('forgotpassword/',Forgot_passwordAPI.as_view()),
   path('userrole_switching/',RoleSwitchingApi.as_view()),
   path('products/',SubcategoryApi.as_view()),
   path('seller_register/',SellerRegisterApi.as_view()),
]