# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS

from . import settings
from .module_one import module_one

# create app
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config.from_object(settings)

# register blueprints/modules
app.register_blueprint(module_one)
