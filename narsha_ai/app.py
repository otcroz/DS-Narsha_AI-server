from flask import Flask, jsonify
from flask import request
from flask_restx import Resource, Api
import boto3
from dotenv import load_dotenv, find_dotenv
import os
# from flask_cors import CORS

## flask server ##
from narsha_ai.chatGPT import ChatGPT

app = Flask(__name__)
api = Api(app, version='0.0.1')

# env #
load_dotenv(find_dotenv())

api.add_namespace(ChatGPT, '/chat')

@api.route('/rekognition/detect-label')
class ObjectDetectionResource(Resource):

    def get(self):
        filename = request.args['filename'] # set params name: filename
        client = boto3.client('rekognition', os.environ["REGION"],
                              aws_access_key_id=os.environ["ACCESS-KEY"],
                              aws_secret_access_key=os.environ["SECRET-KEY"])
        response = client.detect_labels(Image={
            'S3Object': {
                'Bucket': os.environ["BUCKET-NAME"],
                'Name': filename
            }
        },
            MaxLabels=5)

        return jsonify({
                   "result": "success",
                   "label": response["Labels"]
               }, 200)

if __name__ == '__main__' :
    print(os.environ["ACCESS-KEY"])
    app.run(host='127.0.0.1', port=8000)

# CORS(app)
