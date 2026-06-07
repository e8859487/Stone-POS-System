import os
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

import DataParser
from data_repository_factory import get_repository

LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET', '')
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', '')

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# In-memory session per user: {user_id: {state, dataPack}}
sessions = {}

STATE_IDLE = 'idle'
STATE_CONFIRM = 'confirm'


def get_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = {'state': STATE_IDLE, 'dataPack': None}
    return sessions[user_id]


def handle_webhook(body, signature):
    handler.handle(body, signature)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    session = get_session(user_id)

    reply_text = process_message(user_id, text, session)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )


def process_message(user_id, text, session):
    # --- Confirm state: waiting for user to confirm or cancel ---
    if session['state'] == STATE_CONFIRM:
        if text in ['確認', 'yes', 'YES', 'Yes', '是', '確定', 'ok', 'OK']:
            dataPack = session['dataPack']
            session['state'] = STATE_IDLE
            session['dataPack'] = None

            repo = get_repository()
            isSuccess = repo.add_order(dataPack)
            if isSuccess:
                return ('✅ 訂單已儲存！\n\n'
                        '收件人：{}\n'
                        '數量：{}箱\n'
                        '到貨日期：{}').format(
                            dataPack.name,
                            dataPack.numbersOfPack,
                            dataPack.arrivalDate or '(未填)')
            return '❌ 儲存失敗，請稍後再試。'

        else:
            session['state'] = STATE_IDLE
            session['dataPack'] = None
            return '已取消，輸入新訂單文字或傳送「幫助」查看說明。'

    # --- Idle state ---
    if text in ['幫助', 'help', '?', '？', '說明']:
        return get_help_text()

    # Try AI parser first, fallback to regex
    dataPack = None
    try:
        from ai_parser import parse_with_ai
        dataPack = parse_with_ai(text)
    except Exception:
        pass

    if dataPack is None:
        parser = DataParser.ReDataParser()
        parser.setData(text)
        dataPack = parser.parse()

    if dataPack.name and int(dataPack.numbers) > 0:
        session['state'] = STATE_CONFIRM
        session['dataPack'] = dataPack
        return format_order_preview(dataPack)

    return '無法識別訂單格式。\n\n' + get_help_text()


def format_order_preview(dp):
    lines = [
        '📋 訂單預覽，請確認：',
        '',
        '收件人：{}'.format(dp.name or '(未填)'),
        '電話：{}'.format(dp.phone or '(未填)'),
        '手機：{}'.format(dp.mPhone or '(未填)'),
        '地址：{}'.format(dp.address or '(未填)'),
        '數量：{} 件 / {} 箱'.format(dp.numbers, dp.numbersOfPack),
        '到貨日期：{}'.format(dp.arrivalDate or '(未填)'),
        '到貨時段：{}'.format(dp.arrivalTimeFormat),
        '付款方式：{}'.format(dp.paymentMethodFormat),
        '',
        '回覆「確認」儲存，回覆其他任意文字取消。',
    ]
    return '\n'.join(lines)


def get_help_text():
    return (
        '📌 使用方式：\n\n'
        '貼上訂單文字即可自動解析，例如：\n\n'
        '收件人：王小明\n'
        '電話：0912-345-678\n'
        '地址：花蓮市中正路1號\n'
        '數量：8箱\n'
        '到貨日期：10/20\n'
        '下午配送\n'
        '貨到付款\n\n'
        '解析後機器人會顯示預覽，\n'
        '回覆「確認」即寫入 Google Sheets。'
    )
