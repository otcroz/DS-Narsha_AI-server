from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
from PIL import Image, ImageFilter
import io
import torch
import argparse
import base64
import cv2
import numpy as np
import json
import os

ImageMasking = Namespace('ImageMasking')
models = {} # yolov5 models
convert_image_arr = [] # binary to image
# detect_results_arr = {'result': [], 'size': []}  # results
masking_results_arr = {'result': [], 'size': [], 'image': []}

# setting
def yolov5_model():
    # yolov5 setting
    parser = argparse.ArgumentParser(description='Flask API exposing YOLOv5 model')
    parser.add_argument('--port', default=8000, type=int, help='port number')
    parser.add_argument(
        '--model',
        nargs='+',
        default=['nersha_yolo5_model_ysy'],
        help='model(s) to run, i.e. --model nersha_yolo5_model_ysy'
    )
    opt = parser.parse_args()

    for m in opt.model:
        models[m] = torch.hub.load(
            'ultralytics/yolov5',
            'custom',
            path='./models/last.pt',
            force_reload=True,
            skip_validation=True
        )

        print(models)


@ImageMasking.route('/object-detect/<model>')
class ObjectDetect(Resource):
    def post(self, model):
        if request.json.get('images'):
            binary_images = request.json['images'][0]
            file_binary = binary_images.split(',')

            # convert binary to image
            for i in range(len(file_binary)):
                convert_image_arr.append(base64.b64decode(file_binary[i]))

            # detect object
            detect_and_apply_mask(model, convert_image_arr)

            convert_image_arr.clear()

            return_arr = masking_results_arr.copy()

            # setting
            masking_results_arr.clear()
            masking_results_arr['result'] = []
            masking_results_arr['image'] = []
            masking_results_arr['size'] = []

            print(return_arr)

            return return_arr

        else:
            return "null, images not translate."

def detect_and_apply_mask(model, images):
    print("images", len(images))
    for image in images:  # images
        im = Image.open(io.BytesIO(image))

        # 이미지 마스킹 처리 완료한 이미지(인코딩을 한 상태로) 배열에 넣기
        if model in models:
            results = models[model](im, size=640)
            results.print( )
            result = json.loads(results.pandas().xyxy[0].to_json(orient='records'))

            # detect_results_arr['result'].append(result) # add result in list
            # detect_results_arr['size'].append(im.size)  # add result in size


            masking_results_arr['result'].append(result)
            masking_results_arr['size'].append(im.size)  # add result in size

            if result:
                # 첫 이미지 설정
                masked_image = image
                for data in result:
                    # 이미지당 이미지 마스킹 처리하기
                    masked_image = masking_image(masked_image, int(data['xmin']), int(data['ymin']), int(data['xmax']), int(data['ymax']))

                # 이미지를 base64로 인코딩
                image_base64 = base64.b64encode(masked_image).decode('utf-8')
                masking_results_arr['image'].append(image_base64)
            else:
                # 개인정보 없는 이미지 반환
                image_base64 = base64.b64encode(image).decode('utf-8')
                masking_results_arr['image'].append(image_base64)


def masking_image(image, xmin, ymin, xmax, ymax):
    if image:
        # 이미지 형태로 변환
        image_data = Image.open(io.BytesIO(image))

        # 이미지 객체에서 NumPy 배열 형태로 변환
        image_array = np.array(image_data)

        # 모자이크할 영역 추출
        object_region = image_array[ymin:ymax, xmin:xmax]

        # 모자이크 처리
        mosaic_size = (10, 10)  # 모자이크 블록 크기
        object_region = cv2.resize(object_region, mosaic_size, interpolation=cv2.INTER_NEAREST)
        object_region = cv2.resize(object_region, (xmax - xmin, ymax - ymin), interpolation=cv2.INTER_NEAREST)

        # 모자이크 처리한 영역 다시 원본 이미지에 삽입
        image_array[ymin:ymax, xmin:xmax] = object_region

        # NumPy 배열에서 이미지 객체로 변환
        res = Image.fromarray(image_array)

        # 이미지 객체를 바이너리로 변환
        with io.BytesIO() as buffer:
            res.save(buffer, format="PNG")
            image_binary = buffer.getvalue()

    return image_binary
