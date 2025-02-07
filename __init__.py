from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import joblib
from flask_jwt_extended import  JWTManager
from flask_socketio import SocketIO
db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://avnadmin:AVNS_MYsjyNHzbP9d7E_1DVg@pg-208c3d4f-strategy.e.aivencloud.com:20377/defaultdb?sslmode=require"
app.config['JWT_SECRET_KEY'] = 'supersecretkey'


db.init_app(app)
jwt = JWTManager(app)

socketio = SocketIO(app, cors_allowed_origins="*")

