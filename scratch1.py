#!/usr/bin/env python3

#https://www.bing.com/search?q=fanta+orange+price

from urllib.request import Request, urlopen
from statistics import mean, StatisticsError
import re

def gen_urls(urls):
	while True:
		for url in urls.keys():
			yield url


regex = b'\$(\d+.\d+)'
pattern = re.compile(regex)
search_urls = ['http://search.aol.com/aol/search?s_it=topsearchbox.search&s_chn=prt_bon12&v_t=comsearch&q=',
			   'https://www.bing.com/search?q=',
				'https://search.yahoo.com/search?p=',
				'http://www.ask.com/web?q=']
error_terms = {}
#terms = []
dict_urls = {}
miss_count_max = len(search_urls) 
for url in search_urls:
	dict_urls[url] = 0

urls = gen_urls(dict_urls)
with open('terms') as terms:
	for term in terms:
		term = term.strip('\n')
		miss_count = 0
		while True and miss_count < miss_count_max:
			try:
				cur_url = next(urls)
				req = Request(cur_url + term.replace(' ', '+') + 'price')
				with urlopen(req) as response:
					htmltxt = response.read()
					bytes_prices = re.findall(pattern, htmltxt)
					float_prices = []
					print(bytes_prices)
					for price in bytes_prices:
						try:
							float_prices.append(float(price))
						except:
							pass
					print(term, "{:.2f}".format(mean(float_prices)))
					dict_urls[cur_url] += 1
					miss_count = 0
					break
			except StatisticsError:
				pass
			except Exception as e:
				error_terms[term] = str(e) + ';' + cur_url
			finally:
				if miss_count == miss_count_max:
					error_terms.append(term)
				miss_count += 1

print(dict_urls)
print('Error Terms:', error_terms)