import configparser
import pathlib
from distutils.log import Log
Logger = Log()
SettingFilePath = pathlib.Path(__file__).parent.joinpath("SETTING.ini")
config = configparser.ConfigParser()
if (not SettingFilePath.exists()):
    Logger.error("[err] Setting file not found"+ SettingFilePath.as_posix())

config.read(SettingFilePath.as_posix())
FlaskSecretKey = config['default']['FlaskSecretKey']

Sender = config['DataPack']['Sender']
SendersAddress = config['DataPack']['SendersAddress']
SendersMobilePhone = config['DataPack']['SendersMobilePhone']
SalePrice = config['DataPack']['SalePrice']

Scopes = config['GoogleSpreadSheet']['SCOPES']
GOOGLE_SPREADSHEET_URL = config['GoogleSpreadSheet']['GOOGLE_SPREADSHEET_URL']

import re
_match = re.match(r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)', GOOGLE_SPREADSHEET_URL)
if _match:
    SPREADSHEET_ID = _match.group(1)
else:
    SPREADSHEET_ID = None

# Firebase
FIREBASE_KEY_PATH = config.get('Firebase', 'SERVICE_ACCOUNT_KEY_PATH', fallback=None)
DATA_BACKEND = config.get('Database', 'DATA_BACKEND', fallback='google_sheets')

# DeepSeek
DEEPSEEK_API_KEY = config.get('DeepSeek', 'API_KEY', fallback=None)
DEEPSEEK_MODEL = config.get('DeepSeek', 'MODEL', fallback='deepseek-chat')

# LINE Bot
LINE_CHANNEL_SECRET = config.get('LineBot', 'LINE_CHANNEL_SECRET', fallback='')
LINE_CHANNEL_ACCESS_TOKEN = config.get('LineBot', 'LINE_CHANNEL_ACCESS_TOKEN', fallback='')
