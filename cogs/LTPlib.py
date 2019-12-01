import re
from datetime import datetime, timedelta, timezone


# 正規表現オブジェクト
reg_q = re.compile(r'^(「|｢)(.*)(」|｣)$')
reg_a = re.compile(r'^(『|『)(.*)(』|』)$')
reg_reply = re.compile(r'^\D(\d+)\s.*$')

# 遅延時間を秒で指定
DELAY_SECONDS = 120
DELAY_SECONDS_LONGER = 180


# 定型文生成関数
def template(s1: str, s2: str, s3: str) -> str:
    return f"{s1}: {s2} : {s3}" if s3 else f"{s1}: {s2}"


# 現在の日本時間取得
def jst_now() -> str:
    JST = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(JST).strftime("%Y/%m/%d %H:%M")


# 数字か否か判定
def is_num(s: str) -> bool:
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True
