from flask import Flask, request, jsonify

app = Flask(__name__)

app.config.from_object('config')



@app.route('/')
def index():
    return "Hello world"
