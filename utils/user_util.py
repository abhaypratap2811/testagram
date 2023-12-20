import sys
import jwt
import time
from datetime import datetime, timedelta
sys.path.append('./')
from config_data.config import USER_LOGIN_SECRET_KEY

class CustomException(Exception):
    """
    This class is used for CustomExceptions
    """

    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def generate_jwt_token(user_info, secret_key=USER_LOGIN_SECRET_KEY):
    token_for_1_hour = datetime.now() + timedelta(hours=1)
    return jwt.encode({'user_info': user_info, 'exp': time.mktime(token_for_1_hour.timetuple())}, secret_key,
                      algorithm="HS256")


def decode_jwt_token(request):
    try:
        token = request if isinstance(request, str) else request.headers.get('token')
        try:
            user_info = jwt.decode(token, USER_LOGIN_SECRET_KEY, algorithms=["HS256"])
            return user_info
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            raise CustomException("auth_expired", 403)
    except CustomException as e:
        raise CustomException(e.message, e.status_code)