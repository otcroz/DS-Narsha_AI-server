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
from soynlp.normalizer import *
from konlpy.tag import Okt
from soynlp.tokenizer import RegexTokenizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

## file ##
from text_labeling import kobert_text
from text_labeling import replace_word

max_len = 64
batch_size = 64
text_count = 0
res_arr = {"input": [], "result": []}

TextFiltering = Namespace('TextFiltering')


@TextFiltering.route('/curse-filter')
class LimeTextFiltering(Resource):
    def post(self):
        global text_count
        global res_arr

        # preprocessing input
        okt = Okt()
        stop_words = "가 가까스로 가령 가서 가지 각 각각 각자 각종 갖고말하자면 같 같다 같은 같이 개의치않고 거니와 거바 거의 것 것과 것들 게다가 게우다 겨우 견지에서 결과에 결국 결론을 겸사겸사 경우 고려하면 고로 곧 공동으로 과 과연 관계가 관계없이 관련이 관하여 관한 관해서는 구 구체적으로 구토하다 그 그것 그녀 그들 그때 그래 그래도 그래서 그러 그러나 그러니 그러니까 그러면 그러므로 그러한즉 그런 그런데 그런즉 그럼 그럼에도 그렇 그렇게 그렇지 그렇지만 그렇지않으면 그리고 그리하여 그만이다 그에 그위에 그저 그중에서 그치지 근거로 근거하여 기대여 기점으로 기준으로 기타 김에 까닭에 까닭으로 까악 까지 까지도 꽈당 끙끙 끼익 나 나머지는 나오 남들 남짓 낫다 내 낼 너 너희 너희들 네 넷 년 년도 논하지 놀라다 놓 누가 누구 다른 다만 다섯 다소 다수 다시 다시말하면 다음 다음에 다음으로 단지 달려 답다 당신 당장 대로 대하 대하면 대하여 대해 대해서 댕그 더 더구나 더군다나 더라도 더불어 더욱더 더욱이는 데 도달하다 도착하다 동시에 동안 되 되는 되다 되어 된바에야 된이상 두 두번째로 둘 둥둥 뒤따라 뒤이어 든간에 들 들면 들자면 듯하다 등 등등 딩동 따라 따라서 따르 따르는 따름이다 따위 따지지 딱 때 때가 때문 때문에 또 또한 뚝뚝 라 령 로 로부터 로써 륙 를 마음대로 마저 마저도 마치 막론하고 만 만들 만약 만약에 만은 만이 만일 만큼 많 많은 말 말하 말하면 말하자면 말할것도 매 매번 메쓰겁다 명 몇 모 모두 모르 몰라도 몰랏다 못하 못하다 무렵 무릎쓰고 무슨 무엇 무엇때문에 문제 물론 미치다 및 바꾸어말하면 바꾸어말하자면 바꾸어서 바꿔 바로 바와같이 밖에 반대로 반드시 받 방면으로 버금 번 보 보는데서 보다더 보드득 보면 보아 보이 본대로 봐 봐라 부류의 부터 불구하고 불문하고 붕붕 비걱거리다 비교적 비길수 비로소 비록 비슷하다 비추어 비하면 뿐만 뿐만아니라 뿐이다 삐걱 삐걱거리다 사 사람 사람들 사실 사회 살 삼 상대적으로 생각 생각이다 생각하 생각한대로 서술한바와같이 설령 설마 설사 셋 소생 소인 속 솨 수 쉿 습니까 습니다 시각 시간 시작하여 시초에 시키 시키다 실로 심지어 싶 쓰여 씨 아 아니 아니나다를가 아니다 아니라 아니라면 아니면 아니었다면 아래윗 아무거나 아무도 아야 아울러 아이 아이고 아이구 아이야 아이쿠 아하 아홉 안 안다 안된다 않 않고 않기 않는다면 않다 않다면 않도록 않으면 알 알겠는가 알았어 앗 앞 앞에서 앞의것 야 약간 양자 어 어기여차 어느 어느것 어느곳 어느때 어느쪽 어느해 어디 어때 어떠한 어떤 어떤것 어떤것들 어떻 어떻게 어떻해 어이 어째서 어쨋든 어쩔수 어찌 어찌됏든 어찌됏어 어찌하든지 어찌하여 언제 언젠가 얼마 얼마간 얼마나 얼마든지 얼마만큼 얼마큼 없 없고 없다 엉엉 에 에게 에서 여 여기 여덟 여러분 여보시오 여부 여섯 여자 여전히 여차 연관되다 연이서 영 영차 옆사람 예 예를 예컨대 예하면 오 오로지 오르다 오자마자 오직 오호 오히려 와 와르르 와아 왜 왜냐하면 외에 외에도 요만큼 요만한 요만한걸 요컨대 우르르 우리 우리들 우선 우에 운운 원 월 위에서 위하 위하여 위해서 윙윙 육 으로 으로서 으로써 을 응 응당 의 의거하여 의지하여 의해 의해되다 의해서 이 이것 이곳 이때 이라면 이래 이러이러하다 이러한 이런 이럴정도로 이렇 이렇게 이렇게되면 이렇게말하자면 이렇구나 이로 이르기까지 이르다 이리하여 이만큼 이번 이봐 이상 이어서 이었다 이와 이와같다면 이외에도 이용하여 이유는 이유만으로 이젠 이지만 이쪽 이천구 이천육 이천칠 이천팔 인 인젠 인하여 일 일것이다 일곱 일단 일때 일반적으로 일지라도 임에 입각하여 입장에서 잇따라 있 있다 자 자기 자기집 자마자 자신 잘 잠깐 잠시 저 저것 저것만큼 저기 저쪽 저희 적 전 전부 전자 전후 점 점에서 정도 정도에 정도의 제 제각기 제외하고 조금 조차 조차도 졸졸 좀 종합한것과같이 좋 좋아 좍좍 주 주룩주룩 주저하지 줄 줄은 줄은모른다 중 중에서 중의하나 즈음하여 즉 즉시 지 지경이다 지금 지든지 지만 지말고 진짜로 집 쪽으로 차라리 참 참나 첫번째로 쳇 총적으로 칠 콸콸 쾅쾅 쿵 크 타다 타인 탕탕 토하다 통하 통하여 툭 퉤 틀림없다 틈타 팍 팔 퍽 펄렁 편이 하 하게될것이다 하게하다 하겠는가 하고 하고있었다 하곤하였다 하구나 하기 하기는한데 하기만 하기보다는 하기에 하나 하느니 하는 하는것도 하는것만 하는것이 하는바 하다 하더라도 하도다 하도록시키다 하도록하다 하든지 하려고하다 하마터면 하면 하면된다 하면서 하물며 하여금 하여야 하자마자 하지 하지마 하지마라 하지만 하하 한 한다면 한데 한마디 한적이있다 한켠으로는 한하다 한항목 할 할때 할만하다 할망정 할뿐 할수록 할수있다 할수있어 할줄알다 할지라도 할지언정 함께 함으로써 해도 해도된다 해도좋다 해봐요 해서는 해야한다 해요 했어요 향하다 향하여 향해서 허 허걱 허허 헉 헉헉 헐떡헐떡 형식으로 혹시 혹은 혼자 후 훨씬 휘익 휴 흐흐 흥 힘이 힘입어"

        input = request.get_json()
        input = input['input'].split('.')  # split sentence

        # 1) 한글만 추출
        text_list = []
        for i in input:
            i = only_hangle(i)
            text_list.append(i)

        # 2) 형태소만 추출
        text_result = []
        for t in text_list:
            t = okt.morphs(t)
            text_result.append(t)

        # 3) 불용어 필터링
        stop_words = stop_words.split(' ')
        filtering = []
        for result in text_result:
            f = []
            for res in result:
                if res not in stop_words:
                    f.append(res)
            filtering.append(f)

        # 4) 빈 문자열, 중복된 단어 제거하고 한 문장으로 만들기
        preprocess_result = []

        for fi in filtering:
            if len(fi) == 0:
                continue
            text = ''
            for f in fi:
                if f not in text:
                    text += f + " "
            preprocess_result.append(text)

        print(preprocess_result)

        # clear
        res_arr['input'].clear()
        res_arr['result'].clear()

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
