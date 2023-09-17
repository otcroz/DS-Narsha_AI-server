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
res_arr = {"input": [], "result": {}}


TextFiltering = Namespace('TextFiltering')


@TextFiltering.route('/text-filter')
class LimeTextFiltering(Resource):
    def post(self):
        global text_count
        global res_arr

        curse_res_arr = {}
        personal_res_arr = []
        total_curse_arr = []

        # preprocessing input
        input = request.get_json()
        split_sentence = input['input'].split('. ')  # split sentence

        preprocess_result = preprocess.preprocess_text(split_sentence)

        # delete blank item
        personal_sentence = ""
        for idx, item in enumerate(split_sentence):
            if len(item) == 0:
                continue
            if idx == len(split_sentence)-1:
                personal_sentence += item
            else:
                personal_sentence += item + ". "
        res_arr["input"] = personal_sentence

        # define object
        res_object = {
            "curse": [],
            "personal": [],
        }

        for idx, res in enumerate(preprocess_result):
            # 1. check sentence through koBERT
            classify_res = kobert_text.kobert_classify(res)

            if classify_res != 0:
                # split to word unit
                res_temp = res.split(' ')
                # print(res_temp)
                while '' in res_temp:
                    res_temp.remove('')

                if len(res_temp) == 1:  # if word count is 1, except LIME
                    curse_res = replace_word.replace(res_temp[0])
                    curse_res_arr[res_temp] = curse_res
                else:
                    # lime: check curse sentence
                    exp = lime_exp(res)
                    curse_arr = [arr[0] for arr in exp.as_list(label=1) if arr[1] > 0.1]

                    # check to exist curse_arr or not
                    if len(curse_arr) == 0:
                        total_curse_arr.append(personal_sentence[idx])
                    else:
                        # curse replace
                        for curse in curse_arr:
                            curse_res = replace_word.replace(curse)
                            curse_res_arr[curse] = curse_res

            # 2. check personal info
            personal_res = replace_word.detect_personal_info(split_sentence[idx])

            if len(personal_res) != 0:
                for item in personal_res:
                    personal_res_arr.append(item)

        # 4. check curse and personal
        if len(total_curse_arr) != 0:  # check curse
            res_object["total"] = total_curse_arr
        else:
            res_object["total"] = [None]

        if len(personal_res_arr) != 0: # check personal
            res_object["personal"] = personal_res_arr
        else:
            res_object["personal"] = [None]

        if len(curse_res_arr) != 0:  # check total curse sentence
            res_object["curse"] = curse_res_arr
        else:
            res_object["curse"] = None

        # total
        if len(curse_res_arr) == 0 and len(personal_res_arr) == 0 and len(total_curse_arr) == 0:
            res_arr["result"] = True
        else:
            res_arr["result"] = res_object

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

    if count < 32:
        count = 32
    elif count > 1000:
        count = 1000

    # print(count)

    return count


def predict(text):
    global text_count

    input_another = []
    for i in range(0, len(text)):
        input_another.append([text[i], '0'])
    # print(input_another)
    # print(len(input_another))

    probas = kobert_text.kobert_classify_lime(input_another, text_count)

    return probas


def lime_exp(input_data):
    global text_count
    global res_arr

    # set text count
    text_count = cal_lime_text_count(input_data)

    explainer = LimeTextExplainer(class_names=['positive', 'negative'])

    exp = explainer.explain_instance(input_data, predict, num_samples=text_count, top_labels=1)

    # save to lime result
    # exp.save_to_file('./res/data.html')

    # print("available_labels: ", exp.available_labels()[0])

    return exp
