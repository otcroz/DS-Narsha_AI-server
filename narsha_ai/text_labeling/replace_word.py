import re

personal_list = []
replace_words_dic = {
    "미친": "대박", "존나": "진짜", "놈": "사람", "년": "사람", "련": "사람", "급식": "학생", "새끼": "사람",
    "새키": "사람", "애미": "엄마", "애비": "아빠", "한남": "한국 남자", "한녀": "한국 여자", "충": "집단", "계집": "여자",
    "자살": "살자", "맘충": "어머니들", "개": "많이", "짱깨": "중국인", "틀딱": "노인", "잼민": "초등학생",
    "ㅁㅊ": "대박", "ㅈㄴ": "진짜", "ㅅㅋ": "사람", "ㅅㄲ": "사람", "조선족": "한국계 중국인", "간나": "여자아이", "꺼져": "저리가",
    "ㄲㅈ": "저리가", "꼬붕": "부하", "ㄷㅊ": "조용히 해", "닥쳐": "조용히 해", "따까리": "부하", "똘마니": "부하",
    "띨빵": "둔한", "아가리": "입", "젠장": "이런", "트롤": "방해하는 사람", "썅": "아이쿠", "또라이": "특이한 사람",
    "도라이": "특이한 사람", "지랄": "헛소리하네", "ㅈㄹ": "헛소리하네", "씨발": "이런", "ㅅㅂ": "이런", "ㅆㅂ": "이런"
}


def replace(input):
    # replace words
    # res = [{key: value} for key, value in replace_words_dic.items() if word.find(key) != -1]

    for key, value in replace_words_dic.items():
        if input.find(key) != -1:
            return value

    return None


def detect_personal_info(input):
    personal_list.clear()  # clear

    # pattern
    national_id_pattern = r'\d{6}-\d{7}'
    passport_pattern = r'[A-Z]\d{3}[A-Z]\d{4}'
    driver_pattern = r'\d{2}-\d{2}-\d{6}-\d{2}'
    credit_pattern = r'\d{4}[ ,-]\d{4}[ ,-]\d{4}[ ,-]\d{4}'
    phone_pattern = r'010[ ,-]\d{4}[ ,-]\d{4}'
    home_telphone_pattern = r'02[ ,-]\d{3}[ ,-]\d{4}'
    email_pattern = r'[\w!-_\.]+@[\w!-_\.]+\.[\w]{2,3}'

    # check
    list_to_string(re.findall(national_id_pattern, str(input)))
    list_to_string(re.findall(passport_pattern, str(input)))
    list_to_string(re.findall(driver_pattern, str(input)))
    list_to_string(re.findall(credit_pattern, str(input)))
    list_to_string(re.findall(phone_pattern, str(input)))
    list_to_string(re.findall(home_telphone_pattern, str(input)))
    list_to_string(re.findall(email_pattern, str(input)))

    return personal_list


def list_to_string(list):
    for item in list:
        personal_list.append(item)
