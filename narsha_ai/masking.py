# import base64
# import io
# import re
#
# import cv2
# import numpy as np
# from PIL import Image
# import pytesseract
# import re
# from flask import request, jsonify
# from flask_restx import Namespace, Resource
#
# Masking = Namespace('Masking')
# personal_list = []
# # 이미지 전처리
# def preprocess_image(image):
#     # 그레이스케일 변환
#     result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # # 이진화
#     # _, result = cv2.threshold(result, 110, 255, cv2.THRESH_BINARY)
#     #
#     # result = cv2.fastNlMeansDenoising(result, None, 10, 7, 21)
#
#
#     # kernel = np.ones((3, 3), np.uint8)
#     # result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
#
#
#     # 노이즈 제거
#     # kernel = np.ones((5, 5), np.uint8)
#     # result = cv2.dilate(gray_image, kernel, iterations=1)
#
#     # # 이진화
#     # _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
#
#     # # 가우시안 블러 적용 (노이즈 제거)
#     # blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
#     #
#     # # 대비 개선 (선택 사항)
#     # alpha = 1.5  # 대비 조절 (1.0은 변화 없음)
#     # beta = 0  # 밝기 조절 (0은 변화 없음)
#     # enhanced_image = cv2.convertScaleAbs(blurred_image, alpha=alpha, beta=beta)
#
#     return result
#
# # 이미지에서 텍스트와 위치 정보와 함께 추출
# def extract_text_and_boxes_from_image(image):
#     # 배포 후 경로 수정 필요
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#     #image = Image.open(image_path)
#     config = ('-l kor+eng --oem 3 --psm 11')
#     text = pytesseract.image_to_string(image, config=config)
#     boxes = pytesseract.image_to_boxes(image, config=config)
#     return text, boxes
#
# def image_masking(image, x1, y1, x2, y2):
#
#     # 이미지의 높이 가져오기
#     h = image.shape[0]
#     print(h)
#     y1 = h - y1
#     y2 = h - y2
#
#     # 마스킹할 색상
#     mask_color = (255, 255, 255, 0)
#     print(x1, x2, y1, y2)
#     # 이미지에서 주어진 좌표 범위에 대한 마스킹 처리
#     cv2.rectangle(image, (x1, y1), (x2, y2), mask_color, thickness=cv2.FILLED)
#
#     return image
#
#     # 마스킹된 이미지 저장
#     # masked_image_path = "masked_image.jpg"
#     # cv2.imwrite(masked_image_path, image)
#
#     # # 마스킹된 이미지 표시 (테스트 목적으로)
#     # cv2.imshow("Masked Image", image)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#
#     return masked_image_path
#
# def list_to_string(list):
#     for i in list:
#         personal_list.append(i)
#
# def process_image(oriImage, image):
#     # 이미지 불러오기
#     #image = cv2.imread(image_path)
#
#     result = ""
#
#     # Pillow 이미지(Image 객체)를 NumPy 배열(openCV용 이미지)로 변환
#     oriImage_np = np.array(oriImage)
#
#     # 이미지에서 텍스트 추출
#     text, boxes = extract_text_and_boxes_from_image(image)
#     print(boxes)
#     print(text)
#
#     # boxes에서 첫번째 필드 가져와서 문자열로 변환
#     matching_box = [line.split(' ')[0] for line in boxes.splitlines()]
#     matching_string = ''.join(matching_box)
#
#     # 개인정보 패턴
#     # national_id_pattern = r'(\d{6}[ ,-]-?[1-4]\d{6})|(\d{6}[ ,-]?[1-4])'  # 주민등록번호 패턴
#     #national_id_pattern = r'^\d{6}[~ ]?\d{7}$'v
#     national_id_pattern1 = r'\d{6}-\d{7}'
#     national_id_pattern2 = r'\d{6}~\d{7}'
#     passport_pattern = r'[A-Z]\d{3}[A-Z]\d{4}'  # 여권번호 패턴
#     driver_pattern = r'\d{2}-\d{2}-\d{6}-\d{2}'  # 운전면허증 번호 패턴
#     credit_pattern = r'\d{4} \d{4} \d{4} \d{4}'  # 신용카드번호 패턴
#     # phone_pattern = r'010[ ,-]\d{4}[ ,-]\d{4}'  # 전화번호/휴대전화번호 패턴
#     # email_pattern = r'([\w!-_\.]+)@([\w!-_\.]+)\.[\w]{2,3}'  # E-Mail/메일주소 패턴
#
#
#     # credit_pattern = r'[34569][0-9]{3}[-~.[ ]][0-9]{4}[-~.[ ]][0-9]{4}[-~.[ ]][0-9]{4}'  # 신용카드번호 패턴
#
#     # 개인정보 데이터
#     #
#     personal_list.clear()
#     list_to_string(re.findall(national_id_pattern1, text))
#     list_to_string(re.findall(national_id_pattern2, text))
#     list_to_string(re.findall(driver_pattern, text))
#     list_to_string(re.findall(passport_pattern, text))
#     list_to_string(re.findall(credit_pattern, text))
#     #personal_list.append(' '.join(s for s in re.findall(passport_pattern, text)))
#
#     #personal_list.append(' '.join(s for s in re.findall(credit_pattern, text)))
#
#     # personal_list.append(re.findall(phone_pattern, text))
#     # personal_list.append(re.findall(email_pattern, text))
#
#     print(personal_list)
#
#     # 개인정보 데이터 문자열로 변환
#     # personal_string = [item for sublist in personal_list for item in sublist if item != '']
#     # print(personal_string)
#
#     # 숫자와 영문자만 추출하는 정규식
#     # pattern = r'[0-9A-Za-z]+'
#     # for list in personal_list:
#     #     result = re.findall(pattern, list)
#     #     print(result)
#
#
#     for personal in personal_list:
#         if personal:
#             personal = personal.replace(" ", "")
#             print("<<" + personal)
#             length = len(personal)
#             indexNo = matching_string.find(personal)
#
#             lines = boxes.splitlines()
#             first_line = lines[indexNo]
#             x1 = int(first_line.split(' ')[1])
#             y1 = int(first_line.split(' ')[2])
#
#             last_line = lines[indexNo + length - 1]
#             x2 = int(last_line.split(' ')[3])
#             y2 = int(last_line.split(' ')[4])
#
#             # openCV로 마스킹 처리하기
#             result = image_masking(oriImage_np, x1, y1, x2, y2)
#
#         # # 마스킹된 이미지 저장
#         # masked_image_path = "masked_image.jpg"
#         # cv2.imwrite(masked_image_path, result)
#     return result
#
# @Masking.route('/mask-image')
# class MaskImage(Resource):
#     def post(self):
#         convert_image_arr = []
#         # if 'images' in request.files:
#         #     uploaded_images = request.files.getlist('images')
#         #     for image in uploaded_images:
#         #         image_pillow = Image.open(io.BytesIO(image.read()))
#         #         text, boxes = extract_text_and_boxes_from_image(image_pillow)
#         #         print(text)
#         #     return "File uploaded successfully."
#         # else:
#         #     return "No files uploaded."
#
#         if request.json.get('images'):
#             binary_images = request.json['images'][0]
#             file_binary = binary_images.split(',')
#
#             for i in range(len(file_binary)):
#                 print("file_binary", len(file_binary))
#                 convert_image_arr.append(base64.b64decode(file_binary[i]))
#
#             results = []
#
#             for image in convert_image_arr:
#                 # bytes를 Pillow 이미지로 변환(Image 객체로 변환)
#                 image_pillow = Image.open(io.BytesIO(image))
#
#                 # 이미지 전처리
#                 image_np = np.array(image_pillow)
#                 preImage = preprocess_image(image_np)
#
#                 # 이미지 마스킹 처리(원본 이미지, 전처리된 이미지)
#                 result = process_image(image_pillow, preImage)
#
#                 # 이미지 데이터를 base64로 인코딩
#                 _, buffer = cv2.imencode(".png", result)  # 이미지를 PNG 형식으로 인코딩
#                 base64_image = base64.b64encode(buffer).decode()  # base64로 변환
#                 results.append(base64_image)
#
#             return jsonify(results)
#
#         else:
#             return "Image Masking fail."
#
# # 주어진 이미지 경로
# image_path = "asset/images/id.jpg"
# image = cv2.imread(image_path)
#
# preImage = preprocess_image(image)
# process_image(image, preImage)
# cv2.imshow("Masked Image", preImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# # result = process_image(image, preImage)
# #
# # cv2.imshow("Masked Image", result)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
# # # 이미지 처리 함수 호출
# # i = process_image(image)
# #
# # # 마스킹된 이미지 표시 (테스트 목적으로)
# # cv2.imshow("Masked Image", i)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
