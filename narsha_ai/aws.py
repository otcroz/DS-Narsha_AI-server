import os
import boto3
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace

AWS = Namespace('AWS')


@AWS.route('/detect-label')
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
