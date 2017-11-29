# -*- coding: utf-8 -*-
from flask import Flask

from . import settings
from .module_one import module_one

# create app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config.from_object(settings)

# register blueprints/modules
app.register_blueprint(module_one)
