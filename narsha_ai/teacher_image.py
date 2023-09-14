from flask import request, jsonify
from flask_restx import Resource, Api, Namespace

import openai
import os

TeacherImage = Namespace('teacher-image')

@TeacherImage.route('/teacher/image')
class CommentMaker(Resource):
    def post(self):
        input = request.get_json()

        # request body 값
        post_image = input["post_image"]

        # set api key
        openai.api_key = os.environ["FLASK_API_KEY"]

        # Call the chat GPT API
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "조건에 맞게 문자를 SNS 댓글처럼 작성하라."},
                {"role": "system", "content": "act as an elementary school teacher"},
                {"role": "system", "content": "write in informal style"},
                {"role": "system", "content": "말투는 다음과 같다. ~했구나의 말투를 사용한다. 사용자의 담임선생님처럼 반응한다."},  # 반말로 작성한다.
                {"role": "system", "content": "대화 상황은 다음과 같다. 선생님이 학생의 SNS글을 보고 댓글을 달아주고 있다. 나는 선생님이다."},
                {"role": "system", "content": "완전한 SNS 댓글처럼 보여야 한다. 연극 대본처럼 누가 말하는지 절대로 명시하지 않는다."},
                {"role": "system", "content": "줄바꿈 문자를 절대 사용하지 않는다. 화자는 너의 지인이다. 친근한 말투로 작성한다. 학생에게 선생님이 말하듯이 작성한다."},
                {"role": "system", "content": "화자는 너보다 어린아이이다. 너는 성인이다. 가르치는 듯한 말투로 작성한다."},
                {"role": "system", "content": "절대로 영어를 사용하지 않는다. 반드시 한국어만을 사용한다."},
                {"role": "system", "content": "문자는 두 문장 이내로 작성한다. 게시글 사진 키워드와 관련있는 내용으로 작성한다. 하지만 사진과 관련한 모든 키워드를 언급할 필요는 없다."},
                {"role": "user", "content": f"1. 게시글 사진 키워드: ${post_image}"},
            ],
            temperature=0.6,
            max_tokens=2048
        )

        message_result = completion["choices"][0]["message"]["content"].encode("utf-8").decode()

        print(message_result)

        return jsonify({"result": message_result})