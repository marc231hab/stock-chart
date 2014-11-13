The python Stock class will be a class that makes a stock an object oriented item so that we can iterate through larger lists of stocks and search for a certain aspect of a stock. I think I am trying to create a class that can help with a portfolio optimizer but I'm not sure I understand what that means entirely..

Currently what my stock class has:
  initializer(takes string of stock symbol, optional param of time period from following list [1y=default,6m,3m,10d,3d,1d] (ps if you put something other than these it will break so don't do that.. and 1m limits what you can do because it lacks enough data points for many things))
  initData() (called as part of initializer)
    goes to yahoo link to collect open, high, low, close, volume and dates and put into numpy arrays referrable using self._(item)
  simple_moving_avg(int period, array with default of closing prices)
    returns numpy array of simple moving average points for each date
  exp_moving_avg(int period, array with default of closing prices)
    returns numpy array of exp moving average points for each date
  MACD(optional params of exp_ma periods set to 12, 26, 9)
    creates numpy array referrable using self._macd
    
matplotlib is useful to plot these points but they are very easy to read as just terminal output as well..

There is also a run.py script that uses a text file with stock symbols and creates an object of a stock and calculates the macd and returns its current value using intraday points for the past 3 days (I was looking for ones with really high values because I think that should mean they have strong upward momentum.. maybe)

Feel free to screw around with this and make commits to this class and just put sort of useful comments in your commit description
