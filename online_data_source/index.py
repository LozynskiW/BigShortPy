from flask import Flask, request

from .query import Query
from .online_data_sources_integrations import YahooFinance
from .util import panda_to_dict

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)


@app.route('/data', methods=['GET'])
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
        online_data_source = YahooFinance()
    else:
        return "Not supported type. Supported types are: yahoo"

    online_data_source.set_query(query=query)

    pandas_data = online_data_source.download_data_from_source(interval=interval)

    return panda_to_dict(pandas_data=pandas_data)
