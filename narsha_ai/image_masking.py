from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
from PIL import Image
import io
import torch
import argparse
import base64
import json
import os

ImageMasking = Namespace('ImageMasking')
models = {} # yolov5 models
convert_image_arr = [] # binary to image
detect_results_arr = {'result': [], 'size': []} # results


# setting
def yolov5_model():
    # yolov5 setting
    parser = argparse.ArgumentParser(description='Flask API exposing YOLOv5 model')
    parser.add_argument('--port', default=8000, type=int, help='port number')
    parser.add_argument('--model', nargs='+', default=['yolov5m'], help='model(s) to run, i.e. --model yolov5m yolov5m')
    opt = parser.parse_args()

    for m in opt.model:
        models[m] = torch.hub.load('ultralytics/yolov5', 'custom', path='./models/last.pt', force_reload=True, skip_validation=True)

        print(models)


@ImageMasking.route('/object-detect/<model>')
class ObjectDetect(Resource):
    def post(self, model):
        print(model)
        if request.json.get('images'):
            binary_images = request.json['images'][0]
            # print(binary_images)
            file_binary = binary_images.split(',')
            # convert binary to image
            for i in range(len(file_binary)):
                # print("hihi"+"file_binary", len(file_binary))
                convert_image_arr.append(base64.b64decode(file_binary[i]))

            detect_object_yolo(model, convert_image_arr) # detect object
            convert_image_arr.clear()

            # image masking(to be added)
            # masking_image()

            return_arr = detect_results_arr.copy()

            # setting
            detect_results_arr.clear()
            detect_results_arr['result'] = []
            detect_results_arr['size'] = []

            print(return_arr)

            return return_arr

        else: return "null, images not translate."

def detect_object_yolo(model, images):
    #print("images", images)
    print("images", len(images))
    for image in images:  # images
        #print("image", image)
        #im_file = image
        #im_bytes = im_file.read()
        im = Image.open(io.BytesIO(image))

        if 'model' in models:
            results = models[model](im, size=640)
            results.print()
            result = results.pandas().xyxy[0].to_json(orient='records')

            detect_results_arr['result'].append(result) # add result in list
            detect_results_arr['size'].append(im.size)  # add result in size

def masking_image():
    print(masking_image)
