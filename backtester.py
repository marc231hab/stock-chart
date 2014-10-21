
#imports
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
import numpy as np
import time
import datetime
import urllib
import pylab

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#matplotlib.rcParams.update({'font.size':10})

#securities to look at
bg_color = '#575757'



def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    down = -seed[seed<0].sum()/n
    up = seed[seed>=0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)
    for i in range(n, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
            
        up = (up*(n-1)+upval)/n
        down = (down*(n-1)+downval)/n
        
        rs = up/down
        rsi[i] = 100.-100./(1.+rs)
        
    return rsi

def k_value(close_vals, high_vals, low_vals, window):
    window = window - 1
    count = window
    k_vals = np.zeros_like(close_vals)
    #loop over length of close value array
    while count < len(k_vals):
        #get min of lows and max of highs
        lmin = min(low_vals[count-window:count+1])
        hmax = max(high_vals[count-window:count+1])
        
        #calculate k and add to karray
        k = (close_vals[count] - lmin)/(hmax - lmin) * 100
        k_vals[count] = k
        count += 1
    return k_vals

def dvalue(karray, da):
    count = da
    days = da-1
    d_vals = np.zeros_like(karray)
    while count < len(karray):
        sum = 0
        for x in karray[count-days:count+1]:
            sum += x
        
        d = sum / da

        d_vals[count] = d
        count += 1
    return d_vals
    
def movingAverage(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas
    
def expMovingAverage(values, window):
    weights = np.exp(np.linspace(-1,0,window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a

def standard_deviation(date, tf,prices):

    sd = []
    sddate = []
    x = tf
   ######
    while x <= len(prices):
        array2consider = prices[x-tf:x]
        standev = array2consider.std()
        sd.append(standev)
        sddate.append(date[x])
        x+=1
    return sddate,sd
    
def bollinger_bands(date, closep, mult,tff):
    bdate = []
    topBand = []
    botBand = []
    midBand = []

    x = tff

    while x < len(date):
        curSMA = movingAverage(closep[x-tff:x],tff)[-1]

        d,curSD = standard_deviation(date, tff,closep[x-tff:x])

        curSD = curSD[0]

        #print curSD
        #print curSMA

        TB = curSMA + (curSD*mult)
        BB = curSMA - (curSD*mult)
        D = date[x]

        bdate.append(D)
        topBand.append(TB)
        botBand.append(BB)
        midBand.append(curSMA)

        x+=1

    return topBand,botBand,midBand

def getData(stock):    
    #def getData(stock,sm,sd,sy,em,ed,ey):
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=6m/csv'
    #url = 'http://ichart.finance.yahoo.com/table.csv?s='+stock+'&d='+em+'&e='+ed+'&f='+ey+'&g=d&a='+sm+'&b='+sd+'&c='+sy+'&ignore=.csv'
    #url = 'http://ichart.finance.yahoo.com/table.csv?s='+stock+'&d=3&e=12&f=20010&g=d&a=0&b=28&c=2010&ignore=.csv'
    f = urllib.urlopen(url)
    i = 0
    while i < 18:
        f.readline()
        i += 1
    #stockFile = stock+'.txt'
    date, closep, highp, lowp, openp, vol = np.loadtxt(f,delimiter=',',unpack=True,converters={0: mdates.strpdate2num('%Y%m%d')})

    #adjustments to use yahoo ichart data for date selection
    '''date, closep, highp, lowp, openp, vol, adj_cls = np.loadtxt(f,delimiter=',',unpack=True,converters={0: mdates.strpdate2num('%Y-%m-%d')})
    date = np.flipud(date)
    closep = np.flipud(closep)
    highp = np.flipud(highp)
    lowp = np.flipud(lowp)
    openp = np.flipud(openp)
    vol = np.flipud(vol)
    adj_cls = np.flipud(adj_cls)'''
    #end of yahoo ichart changes

    date2 = np.arange(len(date))
    x = 0
    y = len(date)
    candleAr = []
        
    while x < y:
        appendLine = date2[x], openp[x], closep[x], highp[x], lowp[x]
        candleAr.append(appendLine)
        x+=1

    return date, date2, closep, highp, lowp, candleAr

####
def emaplot(subplot, close_, date2_):
    Ema1 = expMovingAverage(close_, 50)
    
    ema = "EMA 50"
    
    start = 50
    SP = len(date2_[start:])
    
    subplot.plot(date2_[-SP:],Ema1[-SP:],'#369de1', label=ema, linewidth=1.5)
    return
    
def bollplot(subplot, close_, date2_, date_):
    t, b, m = bollinger_bands(date_, close_, 2, 20)
    sd1 = "+1 Std Dev"
    sd2 = "-1 Std Dev"
    ma = "SMA 20"
    
    end = len(close_)-1
    buy_box = dict(boxstyle="square,pad=.3", fc="g", alpha=0.6)

    '''
    if close_[end] > t[end-21]:
        subplot.text(date2_[end], t[end-21],'B', color='w', weight='bold', ha='center', va='center', bbox=buy_box)
    '''
    start = 20
    SP = len(date2_[start:])
    
    subplot.plot(date2_[-SP:],t[-SP:],'#e4e6e5', label=sd1, linewidth=1.5)
    subplot.plot(date2_[-SP:],m[-SP:], label=ma)
    subplot.plot(date2_[-SP:],b[-SP:],'#e4e6e5', label=sd2, linewidth=1.5)
    return

def candleplot(subplot, array):

    
    candlestick(subplot, array, width=.6, colorup='#53c156', colordown='#ff1717')
    
    subplot.grid(True, color='w')
    subplot.yaxis.label.set_color("w")

    subplot.spines['bottom'].set_color("#5998ff")
    subplot.spines['top'].set_color("#5998ff")
    subplot.spines['left'].set_color("#5998ff")
    subplot.spines['right'].set_color("#5998ff")
    subplot.tick_params(axis='y', colors='w')
    subplot.tick_params(axis='x', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))
    plt.ylabel('Price')
    
    return
    
def rsiplot(subplot, close_, date2_):
    rsilab = "RSI (14)"

    start = 14
    SP = len(date2_[start:])

    rsi = rsiFunc(close_)
    subplot.plot(date2_[-SP:], rsi[-SP:], label=rsilab)
    subplot.set_ylim(0,100)
    subplot.axhline(70, color='r')
    subplot.axhline(30, color='g')
    subplot.grid(False)
    #subplot.fill_between(date2_,rsi,70, where=(rsi>=70), facecolor = 'r', edgecolor= 'r')
    #subplot.fill_between(date2_,rsi,30, where=(rsi<=30), facecolor = 'g', edgecolor= 'g')
    subplot.set_yticks([30,70])
    subplot.spines['bottom'].set_color("#5998ff")
    subplot.spines['top'].set_color("#5998ff")
    subplot.spines['left'].set_color("#5998ff")
    subplot.spines['right'].set_color("#5998ff")
    subplot.tick_params(axis='x', colors='w')
    subplot.tick_params(axis='y', colors='w')
    return

def stochplot(subplot, array1, array2, date2_, Label1, Label2, SP):
    
    
    subplot.axhline(70, color='r')
    subplot.axhline(50, linestyle='--')
    subplot.axhline(30, color='g')
    subplot.plot(date2_[-SP:],array1[-SP:],'#ffbb00',label=Label1, linewidth=1)
    subplot.plot(date2_[-SP:],array2[-SP:],'#ffffff',label=Label2, linewidth=1)
    subplot.grid(False)
    #subplot.fill_between(date2_,array1,array2, where=(array1>=array2), facecolor = '#ffbb00', edgecolor= '#ffbb00')
    #subplot.fill_between(date2_,array1,array2, where=(array1<array2), facecolor = '#ffffff', edgecolor= '#ffffff')
    subplot.set_yticks([30,70])
    subplot.spines['bottom'].set_color("#5998ff")
    subplot.spines['top'].set_color("#5998ff")
    subplot.spines['left'].set_color("#5998ff")
    subplot.spines['right'].set_color("#5998ff")
    subplot.tick_params(axis='x', colors='w')
    subplot.tick_params(axis='y', colors='w')    
    '''
    buy_box = dict(boxstyle="square,pad=.3", fc="g", alpha=0.6)
    sell_box = dict(boxstyle="square,pad=.3", fc="r", alpha=0.6)
    for loc in date2_[-SP:len(date2_)-1]:
        if array1[loc] < 30 and array1[loc+1] > 30:
            #subplot.annotate('watch', (date2_[loc], array1[loc]), xytext=(15, 15), textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
            subplot.text(date2_[loc], array1[loc],'B', color='w', weight='bold', ha='center', va='center', bbox=buy_box)
        if array1[loc] < 70 and array1[loc-1] > 70: 
            subplot.text(date2_[loc], array1[loc],'S', color='w', weight='bold', ha='center', va='center', bbox=sell_box)
    '''
    return

def makelegend():
    leg = plt.legend(loc=2, ncol=1, prop={'size':9},fancybox=True, borderaxespad=0.)
    leg.get_frame().set_alpha(0.2)
    textEd = pylab.gca().get_legend().get_texts()
    pylab.setp(textEd[0:5], color = 'w')
    return

def graph(security, fig):
    #fig = plt.figure(figsize=(8,4), dpi=200, facecolor=bg_color)
    
    #get data
    date, date2, closep, highp, lowp, candleAr = getData(security)

    
    def getDate(n, pos):
        n = round(n)
        if n >= 0 and n < len(date):
            day = mdates.num2date(date[n])
            return day.date()
        else:
            return ""

            
    formatter = mticker.FuncFormatter(getDate)
    
    #candlestick plot
    candle = plt.subplot2grid((8,4), (1,0), rowspan=4, colspan=4, axisbg=bg_color)
    
    candleplot(candle, candleAr)
    #candle.set_xticks(date2)
    #candle.set_xticklabels(date, rotation=45)
    #candle.xaxis.set_major_locator(mticker.MaxNLocator(10))
    #candle.xaxis.set_major_formatter(formatter)
    
    emaplot(candle, closep, date2)
    bollplot(candle, closep, date2, date)
    makelegend()
    
    rsi_chart = plt.subplot2grid((8,4), (0,0), sharex=candle, rowspan=1, colspan=4, axisbg=bg_color)
    rsiplot(rsi_chart, closep, date2)
    makelegend()
    
    k=20
    d=5
    ds=5
    dss=3
    #stochastics plot
    Label1 = '%K('+str(k)+')'
    Label2 = '%D('+str(d)+')'
    Label3 = '%DS('+str(ds)+')'
    Label4 = '%DSS('+str(dss)+')'

    start = k+d+ds+dss
    SP = len(date2[start:])

    k_array = k_value(closep, highp, lowp, k)
    
    d_array = dvalue(k_array, d)
    
    ds_array = dvalue(d_array, ds)
    
    dss_array = dvalue(ds_array, dss)
    
    
    kplot = plt.subplot2grid((8,4), (5,0), sharex=candle, rowspan=1, colspan=4, axisbg=bg_color)
    stochplot(kplot, k_array, d_array, date2, Label1, Label2, SP)
    makelegend()
    
    dplot = plt.subplot2grid((8,4), (6,0), sharex=candle, rowspan=1, colspan=4, axisbg=bg_color)
    stochplot(dplot, d_array, ds_array, date2, Label2, Label3, SP)
    makelegend()
    
    dsplot = plt.subplot2grid((8,4), (7,0), sharex=candle, rowspan=1, colspan=4, axisbg=bg_color)
    stochplot(dsplot, ds_array, dss_array, date2, Label3, Label4, SP)
    makelegend()
    
    plt.setp(rsi_chart.get_xticklabels(), visible=False)
    plt.setp(candle.get_xticklabels(), visible=False)
    plt.setp(kplot.get_xticklabels(), visible=False)
    plt.setp(dplot.get_xticklabels(), visible=False)
    
    dsplot.set_xticks(date2)
    dsplot.set_xticklabels(date, rotation=45)
    dsplot.xaxis.set_major_locator(mticker.MaxNLocator(10))
    dsplot.xaxis.set_major_formatter(formatter)
    
    plt.subplots_adjust(left=.09, bottom=.2, right=.94, top=.94, wspace=.2, hspace=0)

    plt.suptitle(security+' Price',color='w')
    plt.xlabel('Date',color='w')
    #plt.show()
    return plt
#run function

'''def main():
    securities = 'eurusd','audusd','usdbrl','usdjpy','usdcad','corn','us_10_yr'
    stock = raw_input('Enter security: ')

    #while stock not in securities:
    #    print "Invalid security, valid securities:", securities
    #    stock = raw_input('Enter security: ')

    graph(stock)

    return

main()
'''