from flask import Flask, jsonify
from flask_restx import Resource, Api
from dotenv import load_dotenv, find_dotenv

## load yolov5 ##
from image_masking import yolov5_model

## load bert model ##
from text_labeling import kobert_text
# from flask_cors import CORS

## lime ##
from text_labeling import lime

## flask server ##
from aws import AWS
from chatGPT import ChatGPT
from teacher_content import TeacherContent
from teacher_image import TeacherImage
from teacher_image_content import TeacherImageContent
from disgust_content import DisgustContent
from disgust_image import DisgustImage
from disgust_image_content import DisgustImageContent
from friend_content import FriendContent
from friend_image import FriendImage
from friend_image_content import FriendImageContent
from senior_content import SeniorContent
from senior_image import SeniorImage
from image_masking import ImageMasking
from senior_image_content import SeniorImageContent
from text_labeling import lime




app = Flask(__name__)
api = Api(app, version='0.0.1')



# env #
load_dotenv(find_dotenv())

api.add_namespace(AWS, '/rekognition')
api.add_namespace(ChatGPT, '/chat')
api.add_namespace(TeacherContent, '/chat')
api.add_namespace(TeacherImage, '/chat')
api.add_namespace(TeacherImageContent, '/chat')
api.add_namespace(FriendContent, '/chat')
api.add_namespace(FriendImage, '/chat')
api.add_namespace(FriendImageContent, "/chat")
api.add_namespace(SeniorContent, '/chat')
api.add_namespace(SeniorImage, '/chat')
api.add_namespace(SeniorImageContent, "/chat")
api.add_namespace(DisgustContent, '/chat')
api.add_namespace(DisgustImage, "/chat")
api.add_namespace(DisgustImageContent, "/chat")
api.add_namespace(ImageMasking, "/image")
api.add_namespace(lime.TextFiltering, "/lime")


if __name__ == '__main__' :

    # load yolov5m model
    yolov5_model()

    app.run(host='127.0.0.1', port=8000)



# CORS(app)
