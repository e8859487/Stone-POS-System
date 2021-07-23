import pandas as pd
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
SAMPLE_RANGE_NAME = 'A1:AA1000'

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
                SettingFilePath.as_posix(), SCOPES) # here enter the name of your downloaded JSON file
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

def querySpreadSheetData():
    import google.oauth2.credentials
    global values_input, service
    import flask
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

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

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                      range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])
    flask.session['credentials'] = credentials_to_dict(creds)
    return values_input

def config(*args, **kwargs):
    global SAMPLE_SPREADSHEET_ID_input
    SAMPLE_SPREADSHEET_ID_input = kwargs.get('SAMPLE_SPREADSHEET_ID_input', "")

def getSpreadSheetData():
    spreadSheetData = querySpreadSheetData()
    return pd.DataFrame(spreadSheetData[1:], columns=spreadSheetData[0])


if __name__ == '__main__':
    main()

