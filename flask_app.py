from flask import Flask, render_template, jsonify
import DataParser
import Controls
from ReadGoogleExcel import getSpreadSheetData, AddSpreadSheetData, CreateSheet, initService, GoogleMgr
import GlobalSettings

app = Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = GlobalSettings.FlaskSecretKey

@app.route('/')
def index():
    return render_template("index.html", NavIndex=1)

@app.route('/api_parseData', methods=['GET', 'POST'])
def parseData():
    parser = DataParser.ReDataParser()
    parser.setData(flask.request.form['misc-input'])
    dataPack = parser.parse()
    retDict = {"success": 200, "msg": "上傳成功"}
    retDict.update(dataPack.toDict())
    return jsonify(retDict)

@app.route('/api_addNewData', methods=['GET', 'POST'])
def addNewDataToGoogleSpreadSheet():
    parser = DataParser.HtmlFormDataParser()
    parser.setData(flask.request.form)
    dataPack = parser.parse()
    isSuccess = AddSpreadSheetData(dataPack.toGoogleSpreadSheetFormat())
    if isSuccess:
        return jsonify({"isSuccess": True, "msg": "上傳成功"})
    return jsonify({"isSuccess": False, "msg": "上傳失敗"})

@app.route('/api_importDataFromGoogleSpread', methods=['GET', 'POST'])
def importDataFromGoogleSpread():
    # if 'ImportDataFromGoogleSpread' in flask.request.form:
    arrivalDate = str(flask.request.form['GoogleSpreadArrivalDate-input'])
    if arrivalDate == "":
        return jsonify({"isSuccess": False, "msg": "請選擇日期！"})

    Controls.clearOrderData()
    rawDatas = getSpreadSheetData()
    from DataParser import GoogleSpreadDataParser
    parser = GoogleSpreadDataParser()

    import datetime
    arrivalDate = datetime.datetime.strptime(arrivalDate, "%Y-%m-%d")
    strArrivalDate = "{}/{}/{}".format(arrivalDate.year, arrivalDate.month, arrivalDate.day)
    for row in rawDatas[rawDatas['到貨日期'] == strArrivalDate][GoogleSpreadDataParser.interestColumn].iterrows():
        parser.setData(row)
        dataPack = parser.parse()
        Controls.addNewOrderData(dataPack)

    retDict = {"isSuccess": True, "data": Controls.getOrderData()}
    return retDict

    parser = DataParser.HtmlFormDataParser()
    parser.setData(flask.request.form)
    dataPack = parser.parse()
    isSuccess = AddSpreadSheetData(dataPack.toGoogleSpreadSheetFormat())
    if isSuccess:
        return jsonify({"isSuccess": True, "msg": "上傳成功"})
    return jsonify({"isSuccess": False, "msg": "上傳失敗"})

@app.route('/show_orders', methods=['GET', 'POST'])
def show_orders():
    if not initService():
        return flask.redirect('authorize')
    message = ''
    if 'ClearAllOrders' in flask.request.form:
        Controls.clearOrderData()

    orderedDoc = render_template('showOrders.html', message=message)
    return render_template('index.html', table=orderedDoc, NavIndex=1)

@app.route('/new_orders', methods=['GET', 'POST'])
def new_orders():
    if not initService():
        return flask.redirect('authorize')

    orderedDoc = render_template('newOrders.html')
    return render_template('index.html', table=orderedDoc, NavIndex=2)

# === Google API ===
import GlobalSettings
import flask
import requests
import pathlib
import google.oauth2.credentials
import google_auth_oauthlib.flow
SettingFilePath = pathlib.Path(__file__).parent.joinpath("key.json")
SCOPES = [GlobalSettings.Scopes]

@app.route('/OAuth2')
def OAuth2():
    return render_template('index.html', table=print_index_table(), NavIndex=3)

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = SettingFilePath.as_posix()
@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    # credentials = flow.credentials
    GoogleMgr.credientials = flow.credentials
    # flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('show_orders'))

@app.route('/revoke')
def revoke():
    if GoogleMgr.credientials is None:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **GoogleMgr.credientials)

    # credentials = google.oauth2.credentials.Credentials(
    #      **flask.session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        wording = ('Credentials successfully revoked.' + print_index_table())
    else:
        wording = ('An error occurred.' + print_index_table())

    return render_template('index.html', table=wording)


@app.route('/clear')
def clear_credentials():
    GoogleMgr.credientials = None

    # if 'credentials' in flask.session:
    #     del flask.session['credentials']

    wording =  ('Credentials have been cleared.<br><br>' +
            print_index_table())
    return render_template('index.html', table=wording)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'valid': credentials.valid}

def print_index_table():
    return ('<table>' +
            '<tr><td><a href="/test">Test an API request</a></td>' +
            '<td>Submit an API request and see a formatted JSON response. ' +
            '    Go through the authorization flow if there are no stored ' +
            '    credentials for the user.</td></tr>' +
            '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
            '<td>Go directly to the authorization flow. If there are stored ' +
            '    credentials, you still might not be prompted to reauthorize ' +
            '    the application.</td></tr>' +
            '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
            '<td>Revoke the access token associated with the current user ' +
            '    session. After revoking credentials, if you go to the test ' +
            '    page, you should see an <code>invalid_grant</code> error.' +
            '</td></tr>' +
            '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
            '<td>Clear the access token currently stored in the user session. ' +
            '    After clearing the token, if you <a href="/test">test the ' +
            '    API request</a> again, you should go back to the auth flow.' +
            '</td></tr></table>')

# === Google API End ===


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.run('localhost', 8080, debug=True)