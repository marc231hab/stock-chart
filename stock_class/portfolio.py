#portfolio class
import stocks as stk
class Portfolio:
	def __init__(self):
		self.stocks = {}
		self.cash = 0
	
	def add_stock(self, symbol):
		if symbol not in self.stocks.keys():
			self.stocks[symbol] = stk.Stock(symbol)
		else:
			print("Already in Portfolio")

	def list_stocks(self):
		for symbol in self.stocks.keys():
			print(symbol)