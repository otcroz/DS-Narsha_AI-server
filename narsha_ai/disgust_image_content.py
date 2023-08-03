from flask import request, jsonify
from flask_restx import Resource, Api, Namespace

import openai
import os

from chatGPT import ChatGPT

DisgustImageContent = Namespace('DisgustImageContent')

@ChatGPT.route('/disgust/image-content')
class CommentMaker(Resource):
    def post(self):
        input = request.get_json()

        # request body 값
        post_content = input["post_content"]
        post_image = input["post_image"]

        # set api key
        openai.api_key = os.environ["FLASK_API_KEY"]

        # Call the chat GPT API
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "조건에 맞게 문자를 SNS 댓글처럼 작성하라."},
                {"role": "system", "content": "역할은 작성하지 않는다."},
                {"role": "system", "content": "말투는 다음과 같다. 반말로 작성하라. 짜증나고 비난스럽게 말투로 만들어라."},  # 반말로 작성한다.
                {"role": "system", "content": "상황은 다음과 같다. 학생의 SNS 게시글 사진을 보고 댓글을 달아주고 있다. 너는 까칠한 성격을 가진 반 친구 학생이다."},
                {"role": "system", "content": "상황은 작성하지 않는다."},
                {"role": "system", "content": "댓글임을 작성하지 않는다."},
                {"role": "system", "content": "댓글을 까칠한 학생이 작성한 것처럼 만들어라."},
                {"role": "system", "content": "문자는 두 문장 이내로 작성한다. 게시글 사진 키워드와 관련있는 내용으로 작성한다."},
                {"role": "user", "content": f"1. 게시글 사진 키워드: ${post_image}"},
                {"role": "user", "content": f"1. 게시글 내용: ${post_content}"},
            ],
            temperature=0.3,
            max_tokens=2048
        )

        message_result = completion["choices"][0]["message"]["content"].encode("utf-8").decode()

        return jsonify({"result": message_result})