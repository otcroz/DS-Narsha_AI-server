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

TextFiltering = Namespace('TextFiltering')


@TextFiltering.route('/curse-filter')
class LimeTextFiltering(Resource):
    def post(self):
        input = request.get_json()

        input['input'] = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', "", input['input'])

        res = lime_exp(input['input'])

        return res

def predict(text):
    input_another = []
    for i in range(0, len(text)):
        input_another.append([text[i], '0'])
    print(input_another)

    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

    another_test = kobert_text.BERTDataset(input_another, 0, 1, tokenizer, vocab, max_len, True, False)
    input_dataloder = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=4)

    test_model = kobert_text.load_pretrain_bert()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(input_dataloder)):
        out = test_model(token_ids.long(), valid_length, segment_ids.long())
        tensor_logits = out
        #print('tensor_logits: ', tensor_logits)
        probas = F.sigmoid(tensor_logits).detach().numpy()  # tensor to numpy
        #print('probas: ', probas)
        #print('probas: ', probas.shape)

        return probas


def lime_exp(input_data):
    explainer = LimeTextExplainer(class_names=['positive', 'negative'])

    exp = explainer.explain_instance(input_data, predict, num_samples=64, top_labels=1)

    # save to lime result
    exp.save_to_file('./res/data.html')

    print("available_labels: ", exp.available_labels()[0])

    # filtering curse
    if exp.available_labels()[0] == 0:  # contain curse is not
        return True
    else:  # contain curse
        curse_arr = [arr[0] for arr in exp.as_list(label=1) if arr[1] > 0.1]
        print(curse_arr)

        return curse_arr
