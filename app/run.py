from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
import os

app = Flask(__name__)
swagger = Swagger(app)

# 加载 .env 文件中的环境变量
load_dotenv()

flask_env = os.getenv('FLASK_ENV')

if flask_env == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')
print(flask_env)

if __name__ == '__main__':
    from router import b1
    # 加载路由
    app.register_blueprint(b1)
    app.run(host="0.0.0.0")
