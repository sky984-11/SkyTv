

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

app.config.from_object("config.ProductionConfig")


def configure_logging(app):
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

configure_logging(app)


if __name__ == '__main__':
    from router import b1
    # 加载路由
    app.register_blueprint(b1)
    app.run(host="0.0.0.0")