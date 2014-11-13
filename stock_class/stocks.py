#stock analysis class

#imports
import urllib
import numpy as np

#deletable imports
import matplotlib
import matplotlib.pyplot as plt

class ErrorInit(Exception): 
    pass

class Stock:
	def __init__(self, name, duration="1y"):
		self.name = name
		self.duration = duration
		self.initData()

	def initData(self):
		print self.name
		#link for data
		#try:
		link = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+self.name+'/chartdata;type=quote;range='+self.duration+'/csv'
		opened_file = urllib.urlopen(link)
		it = 0
		#skip text lines at start of data
		if self.duration == "10d":
			skip = 28
		elif self.duration == "3d" or self.duration == "1d":
			skip = 20
		else:
			skip = 17
		while it <= skip:
			opened_file.readline()
			it += 1
		#create numpy arrays of data
		self.dates, self._close, self._high, self._low, self._open, self._volume = np.loadtxt(opened_file, delimiter=',', unpack=True)#, converters={0: mdates.strpdate2num('%Y%m%d')})
		self.date_ran = np.arange(len(self.dates))
		#except:
		#raise ErrorInit

	def simple_moving_avg(self, period, array=None):
		if array == None:
			array = self._close
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
			while i < len(array):
				k = i-period
				val = 0
				while k < i:
					val += array[k]
					k+=1
				val = val / period
				sma[i] = val
				i+=1
			return sma
		else:
			print "not enough data"


	def exp_moving_avg(self, period, array=None):
		if array == None:
			array = self._close
		if len(array) > period and period != 0:
			ema = np.zeros(len(array))
			first = 0
			i = 0
			while i < period:
				first += array[i]
				i+=1
			first = first/period
			i = 0
			while i < period:
				ema[i] = first
				i+=1
			k=period
			smoothing = 2./(period+1)
			while k < len(array):
				ema[k] = (array[k]*smoothing)+(ema[k-1]*(1-smoothing))
				k+=1
			return ema
		else:
			print "not enough data"

	def MACD(self,a=12,b=26,sig=9):
		md_line_a = self.exp_moving_avg(a)
		md_line_b = self.exp_moving_avg(b)
		md_line = md_line_a - md_line_b
		sig_lin = self.exp_moving_avg(sig,md_line)
		macd_hist = md_line - sig_lin
		self._macd = macd_hist
		return macd_hist[len(macd_hist)-1]

'''
def main():
	a = Stock("GPRO")
	sma = a.simple_moving_avg(15)
	ema = a.exp_moving_avg(10)
	md = a.MACD()
	plt.plot(md)
	#plt.plot(sma)
	plt.show()

main()
'''

