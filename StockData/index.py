from flask import Flask

app = Flask(__name__)


@app.route("/who_am_i")
def who_am_i():
    return "StockData"


@app.route('/stockdata', methods=['POST'])
def get_stock_data():
    return 'test', 200
