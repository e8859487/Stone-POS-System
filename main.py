import flask
from flask import Flask, render_template
import pandas as pd
from Controls import TryParse, getOrderData
import Controls
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
    # return 'Hello, World!'

@app.route('/show_Orders', methods=['GET', 'POST'])
def show_Orders():
    message = ''
    if flask.request.method == 'POST':
        dataPack = TryParse(flask.request.form['name-input'])
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