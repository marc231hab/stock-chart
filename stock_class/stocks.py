# stock analysis class

# differences required/helpful for python v3 are denoted by #v3

# required imports
from urllib import urlopen
#v3 from urllib.request import urlopen
import numpy as np

# optional imports

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick
#v3 from matplotlib.finance import candlestick_ochl as candlestick

class ErrorInit(Exception): 
    pass

class Stock:
	def __init__(self, name, duration="1y"):
		self._name = name
		self._duration = duration
		self.initData()

	def initData(self):
		print self._name
		#v3 print(self._name)
		# link for data
		link = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+self._name+'/chartdata;type=quote;range='+self._duration+'/csv'
		opened_file = urlopen(link)
		it = 0
		# skip text lines at start of data
		if self._duration == "10d":
			skip = 28
		elif self._duration == "3d" or self._duration == "1d":
			skip = 20
		else:
			skip = 17
		while it <= skip:
			opened_file.readline()
			it += 1
		# create numpy arrays of data
		self._dates, self._close, self._high, self._low, self._open, self._volume = np.loadtxt(opened_file, delimiter=',', unpack=True)#, converters={0: mdates.strpdate2num('%Y%m%d')})
		self._date_ran = np.arange(len(self._dates))

	def simple_moving_avg(self, period, array=None):
		# if no array assigned then use closing prices
		if array == None:
			array = self._close
		# ensure enough data to calculate averages and period isn't 0
		if len(array) >= period and period != 0:
			sma = np.zeros(len(array))
			first = array[0:period].sum()
			first = first/period
			sma[:period] = first
			i = period
			# calculate Simple Moving Average
			while i < len(array):
				k = i-period
				val = array[k:i].sum()
				val = val / period
				sma[i] = val
				i+=1
			# return Simple moving average
			return sma
		else:
			print "not enough data"
			#v3 print("not enough data")
			return np.zeros(10)


	def exp_moving_avg(self, period, array=None):
		# if no array assigned use closing prices
		if array == None:
			array = self._close
		# ensure enough data points to calculate Exponential Moving Average
		if len(array) >= period and period != 0:
			ema = np.zeros(len(array))
			first = array[0:period].sum()
			first = first/period
			# calculate Exponential Moving Average
			ema[:period] = first
			k=period
			smoothing = 2./(period+1)
			while k < len(array):
				ema[k] = (array[k]*smoothing)+(ema[k-1]*(1-smoothing))
				k+=1
			# return Exp Moving Average
			return ema
		else:
			print "not enough data"
			#v3 print("not enough data")
			return np.zeros(10)

	def MACD(self,a=12,b=26,sig=9):
		# calculate parts of MACD Line
		md_line_a = self.exp_moving_avg(a)
		md_line_b = self.exp_moving_avg(b)
		md_line = md_line_a - md_line_b
		# calculate Signal Line
		sig_lin = self.exp_moving_avg(sig,md_line)
		# Calculate MACD Values
		return md_line, sig_lin

	def ROC(self, period=10):
		# calculate Rate of Change values
		if len(self._close) > period and period != 0:
			roc_vals = np.zeros(len(self._close))
			i = period
			while i < len(self._close):
				roc_vals[i] = ((self._close[i]-self._close[i-period])/self._close[i-period])*100
				i+=1
			return roc_vals

	def VWAP(self, period=1):
		# calculate Volume Weight Average Price
		vwap_vals = np.zeros(len(self._close))
		i = 0
		tot_volume = 0
		tot_price = 0
		# for every point in data calculate vwap
		while i < len(self._close):
			tot_price += (self._low[i]+self._high[i]+self._close[i])/3*self._volume[i]
			tot_volume += self._volume[i]
			vwap_vals[i] = tot_price/tot_volume
			i+=1
		return vwap_vals

	def RSI(self, period=14):
		if len(self._close) > period and period != 0:
			# get day to day changes in values
			changes = np.diff(self._close)
			sub_change = changes[:period+1]
			# sum of up and down days
			neg = -sub_change[sub_change<0].sum()/period
			pos = sub_change[sub_change>0].sum()/period
			rs = pos/neg
			rsi_vals = np.zeros(len(self._close))
			# set initial values
			rsi_vals[:period] = 100.-100./(1.+rs)
			# calculate values until end of data
			for i in range(period, len(self._close)):
				change = changes[i-1]
				if change > 0:
					pos_val = change
					neg_val = 0.
				else:
					pos_val = 0.
					neg_val = -change
				pos = (pos*(period-1)+pos_val)/period
				neg = (neg*(period-1)+neg_val)/period
				rs = pos/neg
				rsi_vals[i]=100.-100./(1.+rs)
			#self._rsi = rsi_vals
			return rsi_vals
		else:
			print "not enough data"
			#v3 print("not enough data")
			#self._rsi = np.zeros(10)
			return np.zeros(10)

	def Stochastic(self, k_period=14, d_period=3):
		k_vals = np.zeros(len(self._close))
		d_vals = np.zeros(len(self._close))
		i = k_period-1
		window = k_period-1
		while i < len(self._close):
			lmin = min(self._low[i-window:i+1])
			hmax = max(self._high[i-window:i+1])
			k_vals[i] = 100*((self._close[i]-lmin)/(hmax-lmin))
			i+=1
		d_vals = self.simple_moving_avg(3,k_vals)
		return k_vals, d_vals

	def Standard_dev(self, period, array):
		std_dev = []
		i = period
		while i <= len(array):
			sub = array[i-period:i]
			std_dev.append(sub.std())
			i+=1
		return std_dev

	def Bollinger_Bands(self, mult=2, period=20):
		top = []
		mid = []
		bottom = []
		i = 0
		while i < period-1:
			top.append(0)
			mid.append(0)
			bottom.append(0)
			i+=1
		i = period
		while i <= len(self._close):
			sma = self.simple_moving_avg(20, self._close[i-period:i])[-1]
			sd = self.Standard_dev(20, self._close[i-period:i])[0]
			t = sma + (sd*mult)
			b = sma - (sd*mult)
			top.append(t)
			mid.append(sma)
			bottom.append(b)
			i+=1
		return top, mid, bottom


def main():
	a = Stock("GPRO")
	sma = a.simple_moving_avg(15)
	ema = a.exp_moving_avg(10)
	md,sig = a.MACD()
	rc = a.ROC()
	vw = a.VWAP()
	rs = a.RSI()
	k_vals, d_vals = a.Stochastic()
	t,m,b = a.Bollinger_Bands()
	x=0
	y=len(a._close)
	candleAr = []
	while x < y:
		appendLine = a._date_ran[x], a._open[x], a._close[x], a._high[x], a._low[x]
		candleAr.append(appendLine)
		x+=1
	candle = plt.subplot2grid((8,4), (0,0), rowspan=4, colspan=4)
	macd_plot = plt.subplot2grid((8,4), (4,0), sharex=candle, rowspan=1, colspan=4)
	roc_plot = plt.subplot2grid((8,4), (5,0), sharex=candle, rowspan=1, colspan=4)
	rsi_plot = plt.subplot2grid((8,4), (6,0), sharex=candle, rowspan=1, colspan=4)
	stoch = plt.subplot2grid((8,4), (7,0), sharex=candle, rowspan=1, colspan=4)
	candlestick(candle, candleAr)
	#plt.plot(a._rsi)
	candle.plot(sma)
	candle.plot(ema)
	candle.plot(t,'--')
	candle.plot(m)
	candle.plot(b,'--')
	#candle.plot(vw)
	candle.set_xlim(0,len(candleAr))
	macd_plot.plot(md)
	macd_plot.plot(sig,'--')
	roc_plot.plot(rc)
	rsi_plot.plot(rs)
	stoch.plot(k_vals)
	stoch.plot(d_vals,'--')
	#stoch.fill_between(a._date_ran,k_vals,d_vals, where=(k_vals>=d_vals), facecolor='#00ccff', edgecolor='#00ccff')
	#stoch.fill_between(a._date_ran,k_vals,d_vals, where=(k_vals<d_vals), facecolor='#00ffff', edgecolor='#00ccff')
	plt.setp(candle.get_xticklabels(), visible=False)
	plt.setp(macd_plot.get_xticklabels(), visible=False)
	plt.setp(roc_plot.get_xticklabels(), visible=False)
	plt.setp(rsi_plot.get_xticklabels(), visible=False)
	plt.show()

main()
