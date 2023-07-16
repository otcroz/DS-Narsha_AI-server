from flask import Flask, jsonify
from flask_restx import Resource, Api
from dotenv import load_dotenv, find_dotenv
import os
# from flask_cors import CORS

## flask server ##
from aws import AWS
from chatGPT import ChatGPT

app = Flask(__name__)
api = Api(app, version='0.0.1')

# env #
load_dotenv(find_dotenv())

api.add_namespace(ChatGPT, '/chat')
api.add_namespace(AWS, '/rekognition')


if __name__ == '__main__' :
    print(os.environ["ACCESS-KEY"])
    app.run(host='127.0.0.1', port=8000)

# CORS(app)
