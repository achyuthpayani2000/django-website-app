import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

def get_jwt_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')

# Usage
user = get_user_model().objects.get(email='user@example.com')
jwt_token = get_jwt_token(user)
print(jwt_token)