from e_commerce import settings
import jwt

def authorization(data):
    auth_header = data.context.META.get('HTTP_AUTHORIZATION')
    if auth_header:
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token