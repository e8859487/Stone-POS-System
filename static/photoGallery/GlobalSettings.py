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

client_id = config['Imgur']['client_id']
client_secret = config['Imgur']['client_secret']
access_token = config['Imgur']['access_token']
refresh_token = config['Imgur']['refresh_token']