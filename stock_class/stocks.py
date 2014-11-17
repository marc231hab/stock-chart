#stock analysis class

#imports
import urllib
import numpy as np

#deletable imports
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick

class ErrorInit(Exception): 
    pass

class Stock:
	def __init__(self, name, duration="1y"):
		self._name = name
		self._duration = duration
		self.initData()

	def initData(self):
		print self._name
		#link for data
		link = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+self._name+'/chartdata;type=quote;range='+self._duration+'/csv'
		opened_file = urllib.urlopen(link)
		it = 0
		#skip text lines at start of data
		if self._duration == "10d":
			skip = 28
		elif self._duration == "3d" or self._duration == "1d":
			skip = 20
		else:
			skip = 17
		while it <= skip:
			opened_file.readline()
			it += 1
		#create numpy arrays of data
		self._dates, self._close, self._high, self._low, self._open, self._volume = np.loadtxt(opened_file, delimiter=',', unpack=True)#, converters={0: mdates.strpdate2num('%Y%m%d')})
		self._date_ran = np.arange(len(self._dates))

	def simple_moving_avg(self, period, array=None):
		#if no array assigned then use closing prices
		if array == None:
			array = self._close
		#ensure enough data to calculate averages and period isn't 0
		if len(array) > period and period != 0:
			sma = np.zeros(len(array))
			i = 0
			first = 0
			while i < period:
				first += array[i]
				i+=1
			first = first/period
			i = 0
			while i < period:
				sma[i] = first
				i+=1
			i = period
			#calculate Simple Moving Average
			while i < len(array):
				k = i-period
				val = 0
				while k < i:
					val += array[k]
					k+=1
				val = val / period
				sma[i] = val
				i+=1
			#return Simple moving average
			return sma
		else:
			print "not enough data"


	def exp_moving_avg(self, period, array=None):
		#if no array assigned use closing prices
		if array == None:
			array = self._close
		#ensure enough data points to calculate Exponential Moving Average
		if len(array) > period and period != 0:
			ema = np.zeros(len(array))
			first = 0
			i = 0
			while i < period:
				first += array[i]
				i+=1
			first = first/period
			i = 0
			#calculate Exponential Moving Average
			while i < period:
				ema[i] = first
				i+=1
			k=period
			smoothing = 2./(period+1)
			while k < len(array):
				ema[k] = (array[k]*smoothing)+(ema[k-1]*(1-smoothing))
				k+=1
			#return Exp Moving Average
			return ema
		else:
			print "not enough data"

	def MACD(self,a=12,b=26,sig=9):
		#calculate parts of MACD Line
		md_line_a = self.exp_moving_avg(a)
		md_line_b = self.exp_moving_avg(b)
		md_line = md_line_a - md_line_b
		#calculate Signal Line
		sig_lin = self.exp_moving_avg(sig,md_line)
		#Calculate MACD Values
		macd_hist = md_line - sig_lin
		self._macd = macd_hist

	def ROC(self, period=10):
		#calculate Rate of Change values
		if len(self._close) > period and period != 0:
			roc_vals = np.zeros(len(self._close))
			i = period
			while i < len(self._close):
				roc_vals[i] = ((self._close[i]-self._close[i-period])/self._close[i-period])*100
				i+=1
			self._roc = roc_vals

	def VWAP(self, period=1):
		#calculate Volume Weight Average Price
		vwap_vals = np.zeros(len(self._close))
		i = 0
		tot_volume = 0
		tot_price = 0
		#for every point in data calculate vwap
		while i < len(self._close):
			tot_price += (self._low[i]+self._high[i]+self._close[i])/3*self._volume[i]
			tot_volume += self._volume[i]
			vwap_vals[i] = tot_price/tot_volume
			i+=1
		self._vwap = vwap_vals




def main():
	a = Stock("GPRO","1d")
	sma = a.simple_moving_avg(15)
	ema = a.exp_moving_avg(10)
	a.MACD()
	a.ROC()
	a.VWAP()
	x=0
	y=len(a._close)
	candleAr = []
	while x < y:
		appendLine = a._date_ran[x], a._open[x], a._close[x], a._high[x], a._low[x]
		candleAr.append(appendLine)
		x+=1
	candle = plt.subplot2grid((4,4), (0,0), rowspan=4, colspan=4)
	candlestick(candle, candleAr)
	plt.plot(a._vwap)
	#plt.plot(sma)
	plt.show()

main()


