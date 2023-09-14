import re

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


def detect_personal_info(input):
    personal_info = []

    # pattern
    national_id_pattern = r'\d{6}-\d{7}'
    passport_pattern = r'[A-Z]\d{3}[A-Z]\d{4}'
    driver_pattern = r'\d{2}-\d{2}-\d{6}-\d{2}'
    credit_pattern = r'\d{4}[ ,-]\d{4}[ ,-]\d{4}[ ,-]\d{4}'
    phone_pattern = r'010[ ,-]\d{4}[ ,-]\d{4}'
    email_pattern = r'([\w!-_\.]+)@([\w!-_\.]+)\.[\w]{2,3}'

    # check
    personal_info.append(re.findall(national_id_pattern, input))
    personal_info.append(re.findall(passport_pattern, input))
    personal_info.append(re.findall(driver_pattern, input))
    personal_info.append(re.findall(credit_pattern, input))
    personal_info.append(re.findall(phone_pattern, input))
    personal_info.append(re.findall(email_pattern, input))

    print(personal_info)

    return personal_info
