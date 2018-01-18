# -*- coding: utf-8 -*-
import urllib
def read_text():
	quotes = open('/Users/kevin/Code/python/basic/data/movie_quotes/movie_quotes.txt')
	content_file = quotes.read()
	print(content_file)
	quotes.close()
	check_profanity(content_file)

def check_profanity(text_to_check):
	connection = urllib.urlopen('http://www.wdyl.com/profanity?p='+text_to_check)
	output = connection.read()
	print(output)
	connection.close()
	if 'true' in output:
		print('profanity!')
	elif 'false' in output:
		print('Good!')
	else:
		print('nothing!')

read_text()