# -*- coding: utf-8 -*-

import os
def rename_files():
	file_list = os.listdir('/Users/kevin/Code/python/basic/data/prank/')
	# print(file_list)
	save_path = os.getcwd()
	print('Current working '+save_path)
	os.chdir('/Users/kevin/Code/python/basic/data/prank/')
	for file_name in file_list:
		print('Old_name - '+file_name)
		print('New_name - '+file_name.translate(None, '0123456789'))
		os.rename(file_name, file_name.translate(None, '0123456789'))
	os.chdir(save_path)

rename_files()