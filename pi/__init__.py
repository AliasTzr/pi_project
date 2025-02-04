from flask import Flask
import pandas as pd
import numpy as np
from .vues import app 
from . import models


models.db.init_app(app)