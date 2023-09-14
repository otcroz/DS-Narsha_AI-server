from lime.lime_text import LimeTextExplainer
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from text_labeling import kobert_text
import gluonnlp as nlp
from tqdm import tqdm, tqdm_notebook
from kobert_tokenizer import KoBERTTokenizer
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import re

max_len = 64
batch_size = 64
text_count = 0

TextFiltering = Namespace('TextFiltering')


@TextFiltering.route('/curse-filter')
class LimeTextFiltering(Resource):
    def post(self):
        global text_count

        input = request.get_json()

        # preprocessing input
        preprocess = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', "", input['input'])

        # set text count
        text_count = cal_lime_text_count(preprocess)

        # lime
        res = lime_exp(preprocess)

        return res


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

    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

    another_test = kobert_text.BERTDataset(input_another, 0, 1, tokenizer, vocab, max_len, True, False)
    input_dataloder = torch.utils.data.DataLoader(another_test, batch_size=64, num_workers=4)

    test_model = kobert_text.load_pretrain_bert()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(input_dataloder)):
        out = test_model(token_ids.long(), valid_length, segment_ids.long())
        tensor_logits = out
        # print('tensor_logits: ', tensor_logits)
        probas = F.sigmoid(tensor_logits).detach().numpy()  # tensor to numpy
        # print('probas: ', probas)
        # print('probas: ', probas.shape)

        return probas


def lime_exp(input_data):
    global text_count

    explainer = LimeTextExplainer(class_names=['positive', 'negative'])

    exp = explainer.explain_instance(input_data, predict, num_samples=64, top_labels=1)

    # save to lime result
    # exp.save_to_file('./res/data.html')

    print("available_labels: ", exp.available_labels()[0])

    # filtering curse
    if exp.available_labels()[0] == 0:  # contain curse is not
        return True
    else:  # contain curse
        curse_arr = [arr[0] for arr in exp.as_list(label=1) if arr[1] > 0.1]
        print(curse_arr)

        return curse_arr
