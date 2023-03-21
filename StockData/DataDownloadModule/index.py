from flask import Flask, jsonify, request

import OnlineDataSource
from QueryAssistanceModule.Query import Query

app = Flask(__name__)

@app.route('/data/', methods=['GET'])
def get_data():
    online_data_source = None

    source = request.args.get('source')
    symbol = request.args.get('symbol')
    country = request.args.get('country')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    interval = request.args.get('interval')

    query = Query(end_date=from_date,
                  start_date=to_date,
                  company=symbol,
                  country=country
                  )

    if source == 'yahoo':
        online_data_source = OnlineDataSource.YahooFinance()
    else:
        return "Not supported type. Supported types are: yahoo"

    online_data_source.set_query(query=query)

    return online_data_source.download_data_from_source(interval=interval)
