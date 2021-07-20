import flask
from flask import Flask, render_template
import pandas as pd

import DataParser
from Controls import getOrderData
import Controls
from ReadGoogleExcel import getSpreadSheetData

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/show_Orders', methods=['GET', 'POST'])
def show_Orders():
    message = ''
    if 'ImportDataFromGoogleSpread' in flask.request.form:
        rawDatas = getSpreadSheetData()
        from DataParser import GoogleSpreadDataParser
        parser = GoogleSpreadDataParser()
        arrivalDate = str(flask.request.form['GoogleSpreadArrivalDate-input'])
        import datetime
        arrivalDate = datetime.datetime.strptime(arrivalDate, "%Y-%m-%d")
        strArrivalDate = "{}/{}/{}".format(arrivalDate.year, arrivalDate.month, arrivalDate.day)
        for row in rawDatas[rawDatas['到貨日期'] == strArrivalDate][GoogleSpreadDataParser.interestColumn].iterrows():
            dataPack = parser.parse(row)
            Controls.addNewOrderData(dataPack)

    elif 'ClearAllOrders' in flask.request.form:
        Controls.clearOrderData()
    elif 'addNewOrder' in flask.request.form:
        parser = DataParser.ReDataParser()
        dataPack = parser.parse(flask.request.form['name-input'])
        dataPack.shippingDate = str(flask.request.form['shippingDate-input']).replace('-', '/')
        dataPack.arrivalDate = str(flask.request.form['arrivalDate-input']).replace('-', '/')
        message = dataPack.formatString()
        Controls.addNewOrderData(dataPack)
    orderedDoc = render_template('Ordered.html', table=getOrderData(), message=message)
    return render_template('index.html', table=orderedDoc)

@app.route("/tables")
def show_tables():
    a = pd.read_csv("0525.csv", encoding='utf-8')
    orderedDoc = render_template('Ordered.html', table=a.to_html())


    return render_template('view.html', table=str(soup))

    data = pd.read_excel('dummy.xlsx')
    data.set_index(['Name'], inplace=True)
    data.index.name=None
    females = data.loc[data.Gender=='f']
    males = data.loc[data.Gender=='m']
    return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')],
    titles = ['na', 'Female surfers', 'Male surfers'])


if __name__ == '__main__':
    app.run(debug=True)