from urllib2 import Request, urlopen
import json
from pymongo import MongoClient

def go(client, pid):
	size = 1024
	rc = '000'
	stock_symbol = client.recv(size)
	print stock_symbol
        url = 'https://www.quandl.com/api/v3/datasets/WIKI/' + stock_symbol + '.json?rows=1&api_key=tZFMcNCHtfsgXbv3tJX2'
        print url
        request = Request(url)
        response = urlopen(request)

        hit = response.read()

        json_data = json.loads(hit)
        record = dict(zip(json_data['dataset']['column_names'][:6], json_data['dataset']['data'][0][:6]))
        record['symbol'] = json_data['dataset']['dataset_code']

        mclient = MongoClient()

        db_stock = mclient['stock']

        col_daily = db_stock['daily']

        result = col_daily.insert_one(record)
        
	# send reply and close connection
	client.send('CC: {0}; {1}; {2}'.format(rc, pid, result.inserted_id))
	client.close()
	return rc 


