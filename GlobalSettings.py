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

Scopes = config['GoogleSpreadSheet']['SCOPES']
SAMPLE_SPREADSHEET_ID_input = config['GoogleSpreadSheet']['SAMPLE_SPREADSHEET_ID_input']
