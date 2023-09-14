replace_words_dic = {
    "미친": "대박", "존나": "진짜", "놈": "사람", "년": "사람", "련": "사람", "급식충": "학생", "새끼": "사람",
    "새키": "사람", "애미": "엄마", "애비": "아빠", "한남": "한국 남자", "한녀": "한국 여자", "충": "집단", "계집": "여자",
    "자살": "살자", "맘충": "어머니들", "개": "많이", "짱깨": "중국인", "틀딱": "노인", "잼민이": "초등학생",
    "ㅁㅊ": "대박", "ㅈㄴ": "진짜", "ㅅㅋ": "사람", "ㅅㄲ": "사람"
}


def replace(input):
    # replace words
    # res = [{key: value} for key, value in replace_words_dic.items() for word in input if word.find(key) != -1]

    res = []
    for word in input:
        for key, value in replace_words_dic.items():
            if word.find(key) != -1:
                res.append({word: value})
                break
            else:
                res.append({word: None})
                break

    return res