import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Определяет, включен ли режим отладки
    # В случае если включен, flask будет показывать
    # подробную отладочную информацию. Если выключен -
    # - 500 ошибку без какой либо дополнительной информации.
    DEBUG = True
    # Ключ, которые будет исползоваться для подписи
    # данных, например cookies.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # URI используемая для подключения к базе данны
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'text.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 1024 * 1024