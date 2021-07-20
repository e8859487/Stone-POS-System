import configparser

config = configparser.ConfigParser()
config.read('SETTING.ini')

Sender = config['DataPack']['Sender']
SendersAddress = config['DataPack']['SendersAddress']
SendersMobilePhone = config['DataPack']['SendersMobilePhone']

Scopes = config['GoogleSpreadSheet']['SCOPES']
SAMPLE_SPREADSHEET_ID_input = config['GoogleSpreadSheet']['SAMPLE_SPREADSHEET_ID_input']
