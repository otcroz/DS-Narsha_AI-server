from flask import Flask
# from flask_cors import CORS
from flask_restx import Api

from narsha_ai.chatGPT import ChatGPT

app = Flask(__name__)
api = Api(app)

api.add_namespace(ChatGPT, '/api')

# CORS(app)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=8000)
