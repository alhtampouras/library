from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '51ab273a7b16ee7bd10722a5e63cd4c7'
from library import routes

