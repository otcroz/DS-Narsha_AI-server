from lime.lime_text import LimeTextExplainer
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
from tqdm import tqdm, tqdm_notebook
from kobert_tokenizer import KoBERTTokenizer
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace


## file ##
from text_labeling import kobert_text
from text_labeling import replace_word
from text_labeling import preprocess

max_len = 64
batch_size = 64
text_count = 0
res_arr = {"input": [], "result": []}

TextFiltering = Namespace('TextFiltering')


@TextFiltering.route('/text-filter')
class LimeTextFiltering(Resource):
    def post(self):
        global text_count
        global res_arr

        # preprocessing input
        input = request.get_json()
        split_sentence = input['input'].split('. ')  # split sentence
        # print("split_sentence: ", split_sentence)

        preprocess_result = preprocess.preprocess_text(split_sentence)


        # clear
        res_arr['input'].clear()
        res_arr['result'].clear()

        res_arr['input'] = split_sentence

        # start repeat(for)
        for res in preprocess_result:
            res_object = {
                "curse": [],
                "personal": [],
            }

            # 1. check sentence through koBERT
            classify_res = kobert_text.kobert_classify(res)

            if classify_res != 0:
                # set text count
                text_count = cal_lime_text_count(res)

                # lime: check curse sentence
                exp = lime_exp(res)
                curse_arr = [arr[0] for arr in exp.as_list(label=1) if arr[1] > 0.1]

                # check to exist curse_arr or not
                if len(curse_arr) == 0:
                    res_object["curse"].append({"문장": True})  # input sentence
                else:
                    # curse replace
                    for curse in curse_arr:
                        curse_res = replace_word.replace(curse)
                        res_object["curse"].append(curse_res)

            else:
                res_object["curse"].append(None)
            print(res_object)

            # 2. check personal info
            personal_res = replace_word.detect_personal_info(input)
            print(personal_res)

            if len(personal_res) != 0:
                for item in personal_res:
                    res_object["personal"].append(item)
            else:
                res_object["personal"].append(None)

            # 3. check curse and personal
            if len(res_object["personal"]) == 0 and len(res_object["personal"]) == 0:
                res_arr["result"].append(True)
            else:
                res_arr["result"].append(res_object)

        return res_arr


def combi(n, r):
    i = 1
    p = 1
    while i <= r:
        p = p * (n - i + 1) // i
        i += 1
    return p


def cal_lime_text_count(text):
    text_arr = text.split()
    # print(text_arr)
    count = 1

    for i in range(0, len(text_arr)):
        count += combi(len(text_arr), i)

    count += count

    if count < 64:
        count = 64
    elif count > 1000:
        count = 1000

    # print(count)

    return count


def predict(text):
    global text_count

    input_another = []
    for i in range(0, len(text)):
        input_another.append([text[i], '0'])
    print(input_another)
    print(len(input_another))

    probas = kobert_text.kobert_classify_lime(input_another)

    return probas


def lime_exp(input_data):
    global text_count
    global res_arr

    explainer = LimeTextExplainer(class_names=['positive', 'negative'])

    exp = explainer.explain_instance(input_data, predict, num_samples=64, top_labels=1)

    # save to lime result
    # exp.save_to_file('./res/data.html')

    # print("available_labels: ", exp.available_labels()[0])

    return exp
