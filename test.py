#from Tkinter import *
import Tkinter as Tk
import sys


#stock imports
import matplotlib
matplotlib.use('TkAgg')

import backtester

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
import numpy as np
import time
import datetime
import urllib





#build stock chart
bg_color = '#575757'

#def graph(security):

class App(Tk.Frame):

    def __init__(self, parent):
        self.parent = parent
        Tk.Frame.__init__(self)

        self.initUI()
        self._create_menu()

    def initUI(self):
        self.parent.title("Marc's Stock App")

        #date variables
        self.startdatemonthvar = Tk.StringVar()
        self.startdatemonthvar.set("Jan")
        self.startdatedayvar = Tk.IntVar()
        self.startdatedayvar.set(1)
        self.startdateyearvar = Tk.IntVar()
        self.startdateyearvar.set(2013)

        self.enddatemonthvar = Tk.StringVar()
        self.enddatemonthvar.set("Jan")
        self.enddatedayvar = Tk.IntVar()
        self.enddatedayvar.set(1)
        self.enddateyearvar = Tk.IntVar()
        self.enddateyearvar.set(2014)

        #indicator variables
        self.bollvar = Tk.IntVar()
        self.bollvar.set = 0
        self.smavar = Tk.IntVar()
        self.smavar.set = 0
        self.emavar = Tk.IntVar()
        self.emavar.set = 0
        self.rsivar = Tk.IntVar()
        self.rsivar.set = 0
        self.stochvar = Tk.IntVar()
        self.stochvar.set = 0

        #self.style = Style()
        #self.style.theme_use("default")
        self.pack(fill=Tk.BOTH, expand=1)

        topFrame = Tk.Frame(self, relief=Tk.RAISED, borderwidth=1)
        #topFrame.grid(column=1,row=1)
        topFrame.pack(fill=Tk.X)

        midFrame = Tk.Frame(self, relief=Tk.SUNKEN, borderwidth=1)
        #midFrame.grid(column=1,row=2)
        midFrame.pack(fill=Tk.X)

        bottomFrame = Tk.Frame(self, relief=Tk.RAISED, borderwidth=1)
        #bottomFrame.grid(column=1,row=3)
        bottomFrame.pack(fill=Tk.X,side=Tk.BOTTOM)

        #self.pack(fill=BOTH, expand=1)
        self.fig = plt.figure(figsize=(12,6), dpi=80, facecolor=bg_color)

        self.stock_entry = Tk.Entry(topFrame)
        #self.stock_entry.grid(column=1,row=1)
        self.stock_entry.bind('<Return>', self.get_stock)
        self.stock_entry.pack(side=Tk.LEFT)

        self.bollButt = Tk.Checkbutton(topFrame, variable=self.bollvar, text="Bollinger Bands", command=self.new_window)
        self.bollButt.pack(side=Tk.RIGHT)

        self.smaButt = Tk.Checkbutton(topFrame, variable=self.smavar, text="SMA", command=self.new_window)
        self.smaButt.pack(side=Tk.RIGHT)

        self.emaButt = Tk.Checkbutton(topFrame, variable=self.emavar, text="EMA", command=self.new_window)
        self.emaButt.pack(side=Tk.RIGHT)

        self.rsiButt = Tk.Checkbutton(topFrame, variable=self.rsivar, text="RSI", command=self.new_window)
        self.rsiButt.pack(side=Tk.RIGHT)

        self.stochButt = Tk.Checkbutton(topFrame, variable=self.stochvar, text="Stochastics", command=self.new_window)
        self.stochButt.pack(side=Tk.RIGHT)

        self.quitButton = Tk.Button(bottomFrame, text="Quit", command=self.quit)
        self.quitButton.pack(side=Tk.BOTTOM, padx=5, pady=5)

        self.startlabel = Tk.Label(bottomFrame, text="Start Date:")
        self.startlabel.pack(side=Tk.LEFT)
        self.startdatemonth = Tk.OptionMenu(bottomFrame, self.startdatemonthvar, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Sep", "Oct", "Nov", "Dec")
        self.startdatemonth.pack(side=Tk.LEFT)
        self.startdateday = Tk.OptionMenu(bottomFrame, self.startdatedayvar, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
        self.startdateday.pack(side=Tk.LEFT)
        self.startdateyear = Tk.OptionMenu(bottomFrame, self.startdateyearvar, 2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014)
        self.startdateyear.pack(side=Tk.LEFT)

        self.endlabel = Tk.Label(bottomFrame, text="End Date:")
        self.endlabel.pack(side=Tk.LEFT)
        self.enddateyear = Tk.OptionMenu(bottomFrame, self.enddatemonthvar, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Sep", "Oct", "Nov", "Dec")
        self.enddateyear.pack(side=Tk.LEFT)
        self.enddateday = Tk.OptionMenu(bottomFrame, self.enddatedayvar, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
        self.enddateday.pack(side=Tk.LEFT)
        self.enddateyear = Tk.OptionMenu(bottomFrame, self.enddateyearvar, 2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014)
        self.enddateyear.pack(side=Tk.LEFT)

        self.hiButton = Tk.Button(topFrame, text="Submit", command=self.make_graph)
        self.hiButton.grid(column=4,row=1)
        self.hiButton.pack(side=Tk.LEFT)

        self.graphCanvas = FigureCanvasTkAgg(self.fig, midFrame)
        self.graphCanvas.get_tk_widget().pack(side=Tk.TOP,fill=Tk.BOTH, expand=1)


    def say_hi(self):
        print "hi there, everyone!"

    def get_stock(self, event):
        self.make_graph()

    def make_graph(self):
        stock = self.stock_entry.get()
        self.fig.clf()
        backtester.graph(stock, self.fig)
        self.graphCanvas.draw()

    def _create_menu(self):        
        self.mbar = Tk.Menu(self, type='menubar')
        self.parent['menu'] = self.mbar
        # create the 'File' menu
        menu = Tk.Menu(self.mbar, tearoff=0)
        self.mbar.add_cascade(label='File', underline=0, menu=menu )  
        menu.add_command(label='Quit', underline=0, command=self.quit_callback, accelerator='Meta-Q')

    def quit_callback(self):
        self.destroy()
        sys.exit(0)

    def new_window(self):
        self.newWindow = Tk.Toplevel(self.parent)
        self.popup = NotWorkingPopup(self.newWindow)

class NotWorkingPopup:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Tk.Frame(self.parent)
        self.init_wind()
        self.frame.pack()

    def init_wind(self):
        self.notworking = Tk.Label(self.frame, text="This feature is not working yet!")
        self.notworking.pack()
        self.quitButton = Tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()

    def close_windows(self):
        self.parent.destroy()

def main():

    root = Tk.Tk()

    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_callback)
    root.mainloop()

if __name__ == '__main__':
    main()