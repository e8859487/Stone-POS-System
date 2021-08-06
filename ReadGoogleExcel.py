import pandas as pd
import flask
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import GlobalSettings
import pathlib

SettingFilePath = pathlib.Path(__file__).parent.joinpath("key.json")
SCOPES = [GlobalSettings.Scopes]

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = GlobalSettings.SAMPLE_SPREADSHEET_ID_input
TEST_SPREADSHEET_ID_input = GlobalSettings.TEST_SPREADSHEET_ID_input
SAMPLE_RANGE_NAME = 'A1:AA1000'
SHEET_RESPONSE_RANGE = '表單回應 1!A1:R208'  # filled by customers
AUTO_FILL_TABLE_NAME = '全自動資料表'
WEBSITE_RESPONSE_RANGE = '{}!A1:R208'.format(AUTO_FILL_TABLE_NAME)  # filled from website

service = None

def main():
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SettingFilePath.as_posix(), SCOPES)  # here enter the name of your downloaded JSON file
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                      range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    # if not values_input and not values_expansion:
    #     print('No data found.')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def initService():
    import google.oauth2.credentials
    global values_input, service
    if service is not None:
        return True
    if 'credentials' not in flask.session:
        return False

        # Load credentials from the session.
    creds = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    # creds = None
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             SettingFilePath.as_posix(), SCOPES)  # here enter the name of your downloaded JSON file
    #         creds = flow.run_local_server()
    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)
    #
    service = build('sheets', 'v4', credentials=creds)
    flask.session['credentials'] = credentials_to_dict(creds)
    CreateSheet()
    return True


def querySpreadSheetData():
    global service
    if not initService():
        return

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                      range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])
    return values_input

def getSpreadSheetData():
    spreadSheetData = querySpreadSheetData()
    return pd.DataFrame(spreadSheetData[1:], columns=spreadSheetData[0])

def CreateSheet():
    global service
    if not initService():
        return

    #  check sheet existence
    spreadSheets = service.spreadsheets().get(spreadsheetId=TEST_SPREADSHEET_ID_input).execute()
    for sheet in spreadSheets['sheets']:
        sheetTitle = sheet['properties']['title']
        if sheetTitle == AUTO_FILL_TABLE_NAME:
            isSheetExist = True
            break
    else:
        isSheetExist = False

    if not isSheetExist:
        batch_update_spreadsheet_request_body = {
            'requests': [{'addSheet': {
                'properties': {
                    "title": AUTO_FILL_TABLE_NAME,
                }
            }}
            ]
        }
        request = service.spreadsheets().batchUpdate(spreadsheetId=TEST_SPREADSHEET_ID_input,
                                                     body=batch_update_spreadsheet_request_body)
        response = request.execute()
        print("Create New sheet:", AUTO_FILL_TABLE_NAME)
        AddSpreadSheetData([['時間戳記', '收件人', '到貨日期', '指定到貨時段', '住址',
                             '聯絡電話 (04-88xxxxxx)', '手機 (09xx-xxx-xxx)',
                             '數量', '付款方式', '其他需求',
                             '備註', '數量分析', '出貨日期', '套袋']])

def AddSpreadSheetData(rowDatas):
    '''
    :param rowDatas:
    [["valuea1"],
    ["valuea2"],
    ["valuea3"]]
    :return:
    '''
    from pprint import pprint
    global service
    if not initService():
        return

    # The A1 notation of a range to search for a logical table of data.
    # Values will be appended after the last row of the table.
    range_ = WEBSITE_RESPONSE_RANGE  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.

    # list = [["valuea1"], ["valuea2"], ["valuea3"]]
    value_range_body = {
        "majorDimension": "ROWS",
        "values": rowDatas
    }

    request = service.spreadsheets().values().append(
        spreadsheetId=TEST_SPREADSHEET_ID_input, range=range_,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()
    return response

    # pprint(response)


if __name__ == '__main__':
    # AddSpreadSheetData()
    pass
