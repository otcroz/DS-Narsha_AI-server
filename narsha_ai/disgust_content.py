from flask import request, jsonify
from flask_restx import Resource, Api, Namespace

import openai
import os

from chatGPT import ChatGPT

DisgustContent = Namespace('DisgustContent')

@ChatGPT.route('/disgust/content')
class CommentMaker(Resource):
    def post(self):
        input = request.get_json()

        # request body 값
        post_content = input["post_content"]

        # set api key
        openai.api_key = os.environ["FLASK_API_KEY"]

        # Call the chat GPT API
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 학생들이 올린 게시물 내용과 관련된 문장을 작성 해야 해."},
                {"role": "system", "content": "문장은 까칠한 학생이 작성한 것처럼 댓글 형태로 만들어줘."},
                {"role": "system", "content": "문장은 두 문장만 나오게 만들어줘. 문장을 반말 형태로 만들어줘."},
                {"role": "system", "content": f"1. 게시글 내용: ${post_content}"},
            ],
            temperature=0.8,
            max_tokens=2048
        )

        message_result = completion["choices"][0]["message"]["content"].encode("utf-8").decode()

        return jsonify({"result": message_result})