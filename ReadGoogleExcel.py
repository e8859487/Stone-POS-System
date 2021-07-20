import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

import GlobalSettings

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
                'key.json', SCOPES) # here enter the name of your downloaded JSON file
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

def config(*args, **kwargs):
    global SAMPLE_SPREADSHEET_ID_input
    SAMPLE_SPREADSHEET_ID_input = kwargs.get('SAMPLE_SPREADSHEET_ID_input', "")

def getSpreadSheetData():
    main()
    return pd.DataFrame(values_input[1:], columns=values_input[0])


if __name__ == '__main__':
    main()

