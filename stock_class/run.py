#main

import stocks as stk
#from stocks import ErrorInit
#import matplotlib
#import matplotlib.pyplot as plt

nasdaq = open('mini.txt','r')
nasdaq.readline()
nasdaq_list = dict([line.strip().split('\t') for line in nasdaq])
#for key in nasdaq_list:#
#	a=stk.Stock(key)
macd_vals = {}
#portfolio = ["AAPL","GPRO","NEP","TKMR","CHS","HEB","DOW","BABA","AMBA","TSLA","NFLX","IBM","FEYE","SCTY","SFUN","ATSCHH"]
#for sec in portfolio:
for key in nasdaq_list:
	#try:
	a = stk.Stock(key,"3d")
	#except ErrorInit:
#	print key, "didn't work"
	macd_vals[key] = a.MACD()
	#plt.plot(a._macd)
	#plt.show()
for key in macd_vals:
	print key, macd_vals[key]