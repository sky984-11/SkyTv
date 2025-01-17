'''
Description: 
Author: liupeng
Date: 2025-01-16 17:47:07
LastEditTime: 2025-01-17 10:05:30
LastEditors: liupeng
'''
import jwt
from datetime import datetime, timedelta
from config import  BaseConfig



SECRET_KEY = BaseConfig.SECRET_KEY


def generate_token(username,password,exp=3600):
  current_time = datetime.now()
  future_time = current_time + timedelta(minutes=exp) # 默认3600分钟过期
  future_timestamp = future_time.timestamp()
  payload = {
        'exp': future_timestamp,
        'username': username,
        'password': password
    }
  encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
  return encoded_jwt


def decode_token(encoded_jwt):
    try:
        decoded = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=['HS256'])
        if is_token_expired(decoded):
          return {'error': 'Token has expired.'}

        return decoded
    except jwt.ExpiredSignatureError:
        # 如果令牌已过期，可以在这里处理过期的情况
        return {'error': 'Token has expired.'}
    except jwt.InvalidTokenError:
        # 如果令牌无效，可以在这里处理无效令牌的情况
        return {'error': 'Invalid token.'}

def is_token_expired(decoded_token):
    if 'exp' in decoded_token:
        exp_timestamp = decoded_token['exp']
        current_time = datetime.now().timestamp()
        # print(exp_timestamp,current_time)

        if exp_timestamp < current_time:
            return True
    return False


if __name__ == '__main__':
    encoded_jwt = generate_token('sky','123456')
    print(encoded_jwt)

    # 这里使用生成的 token 进行解码示例
    decoded_token = decode_token(encoded_jwt)
    print(decoded_token)
