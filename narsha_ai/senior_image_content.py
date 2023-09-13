from flask import request, jsonify
from flask_restx import Resource, Api, Namespace

import openai
import os

SeniorImageContent = Namespace('SeniorImageContent')

@SeniorImageContent.route('/senior/image-content')
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
                {"role": "system", "content": "문자는 두 문장 이내로 작성한다. 게시글 내용과 관련있는 내용으로 작성한다."},
                {"role": "system", "content": "완전한 SNS 댓글처럼 보여야 한다. 연극 대본처럼 누가 말하는지 절대로 명시하지 않는다."},
                {"role": "system", "content": "act as an school senior."},
                {"role": "system", "content": "write in informal style"},
                {"role": "system", "content": "문자는 두 문장 이내로 작성한다. 게시글 내용과 게시글 사진에 관련있는 내용으로 작성한다. 하지만 사진과 관련한 모든 키워드를 언급할 필요는 없다."},
                {"role": "system", "content": "너는 12살이다. 9살 동생에게 말하는 것처럼 답한다."},
                {"role": "system", "content": "입력문자에 영어가 있어도 절대로 영어를 사용하지 않는다. 반드시 한국어만을 사용한다."},
                {"role": "system", "content": "너는 반말을 한다."},
                {"role": "system", "content": "너는 밝고 친절하고, 장난치는 것을 좋아하는 성격이다."},
                {"role": "system", "content": "줄바꿈 문자를 절대 사용하지 않는다."},
                {"role": "system", "content": "댓글임을 작성하지 않는다."},
                {"role": "user", "content": f"1. 게시글 내용: ${post_content} 2. 게시글 사진: ${post_image}"},
            ],
            temperature=0.6,
            max_tokens=2048
        )

        message_result = completion["choices"][0]["message"]["content"].encode("utf-8").decode()

        return jsonify({"result": message_result})