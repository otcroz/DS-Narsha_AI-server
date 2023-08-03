from flask import Flask, jsonify
from flask_restx import Resource, Api
from dotenv import load_dotenv, find_dotenv
import os

# from flask_cors import CORS

## flask server ##
from aws import AWS
from chatGPT import ChatGPT
from teacher_content import TeacherContent
from teacher_image import TeacherImage
from teacher_image_content import TeacherImageContent
from disgust_content import DisgustContent
from disgust_image import DisgustImage
from disgust_image_content import DisgustImageContent


app = Flask(__name__)
api = Api(app, version='0.0.1')

# env #
load_dotenv(find_dotenv())

api.add_namespace(ChatGPT, '/chat')
api.add_namespace(TeacherContent, '/chat')
api.add_namespace(TeacherImage, '/chat')
api.add_namespace(TeacherImageContent, '/chat')
api.add_namespace(AWS, '/rekognition')
api.add_namespace(DisgustContent, '/chat')
api.add_namespace(DisgustImage, "/chat")
api.add_namespace(DisgustImageContent, "/chat")


if __name__ == '__main__' :
    print(os.environ["ACCESS-KEY"])
    app.run(host='127.0.0.1', port=8000)

# CORS(app)
