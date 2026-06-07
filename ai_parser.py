import json
import base64
import requests
import GlobalSettings
from DataPack import (
    DataPack, ARRIVALTIME_MORNING, ARRIVALTIME_AFTERNOON,
    ARRIVALTIME_NOT_SPECIFIED, PAYMENTMETHOD_TRANSFER, PAYMENTMETHOD_PAY_ON_DELIVERY
)
import math

SYSTEM_PROMPT = """你是一個訂單資料擷取助手。從使用者提供的文字中擷取葡萄訂單資訊。

請以 JSON 格式回傳，欄位如下：
{
  "name": "收件人姓名",
  "phone": "市話（格式：02-12345678）",
  "mPhone": "手機（格式：0912-345-678）",
  "address": "完整地址",
  "arrivalDate": "到貨日期（格式：YYYY/MM/DD）",
  "numbers": 數量（整數，單位：箱）,
  "arrivalTime": "上午 或 下午 或 不指定",
  "paymentMethod": "轉帳 或 貨到付款",
  "userComment": "其他備註"
}

規則：
- 找不到的欄位填空字串 "" 或 0
- 數量單位是「箱」，1件 = 4箱（例如：2件 = 8箱）
- 如果只有月/日沒有年份，年份用 2026
- 手機格式化為 0912-345-678，市話格式化為 02-12345678
- 只回傳 JSON，不要其他文字"""


def parse_with_ai(text):
    """Use DeepSeek to parse order text into a DataPack."""
    api_key = GlobalSettings.DEEPSEEK_API_KEY
    model = GlobalSettings.DEEPSEEK_MODEL

    if not api_key:
        return None

    response = requests.post(
        'https://api.deepseek.com/chat/completions',
        headers={
            'Authorization': 'Bearer {}'.format(api_key),
            'Content-Type': 'application/json',
        },
        json={
            'model': model,
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': text},
            ],
            'temperature': 0,
        },
        timeout=15,
    )
    response.raise_for_status()

    content = response.json()['choices'][0]['message']['content']
    # Strip markdown code fences if present
    content = content.strip()
    if content.startswith('```'):
        content = content.split('\n', 1)[1]
        content = content.rsplit('```', 1)[0]

    data = json.loads(content)
    return _dict_to_datapack(data)


def parse_image_with_ai(image_bytes, content_type='image/jpeg'):
    """Use DeepSeek vision to parse an order image into a DataPack."""
    api_key = GlobalSettings.DEEPSEEK_API_KEY
    model = GlobalSettings.DEEPSEEK_MODEL

    if not api_key:
        return None

    b64 = base64.b64encode(image_bytes).decode('utf-8')
    data_url = 'data:{};base64,{}'.format(content_type, b64)

    response = requests.post(
        'https://api.deepseek.com/chat/completions',
        headers={
            'Authorization': 'Bearer {}'.format(api_key),
            'Content-Type': 'application/json',
        },
        json={
            'model': model,
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': [
                    {'type': 'image_url', 'image_url': {'url': data_url}},
                    {'type': 'text', 'text': '請從這張圖片中擷取訂單資訊'},
                ]},
            ],
            'temperature': 0,
        },
        timeout=30,
    )
    response.raise_for_status()

    content = response.json()['choices'][0]['message']['content']
    content = content.strip()
    if content.startswith('```'):
        content = content.split('\n', 1)[1]
        content = content.rsplit('```', 1)[0]

    data = json.loads(content)
    return _dict_to_datapack(data)


def _dict_to_datapack(d):
    dp = DataPack()
    dp.name = d.get('name', '') or ''
    dp.phone = d.get('phone', '') or ''
    dp.mPhone = d.get('mPhone', '') or ''
    dp.address = d.get('address', '') or ''
    dp.arrivalDate = d.get('arrivalDate', '') or ''
    dp.shippingDate = ''

    numbers = d.get('numbers', 0) or 0
    dp.numbers = str(int(numbers))
    dp.numbersOfPack = str(math.ceil(int(dp.numbers) / 4.0)) if int(dp.numbers) > 0 else '0'

    arrival_time = d.get('arrivalTime', '')
    if arrival_time == '下午':
        dp.arrivalTime = ARRIVALTIME_AFTERNOON
    elif arrival_time == '不指定':
        dp.arrivalTime = ARRIVALTIME_NOT_SPECIFIED
    else:
        dp.arrivalTime = ARRIVALTIME_MORNING

    payment = d.get('paymentMethod', '')
    dp.paymentMethod = PAYMENTMETHOD_PAY_ON_DELIVERY if payment == '貨到付款' else PAYMENTMETHOD_TRANSFER

    dp.userComment = d.get('userComment', '') or ''
    return dp
