from flask import Flask
from flask_restx import Api

# from utils import get_games
app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='тестовое задание',
    description='<I>Выдаем самый новый список из популярнейших игр Steama</I>',
    contact='Мельников Владислав',
    contact_url='https://vk.com/mindoken89',

)
# import routes