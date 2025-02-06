
import datetime
from enum import Enum


class BuySell(Enum):
	BUY = 0
	SELL = 1


class Trade:
	def __init__(self, symbol, timestamp, quantity, price, buy_sell):
		self.symbol = symbol
		self.timestamp = timestamp
		self.quantity = quantity
		self.price = price
		self.buy_sell = buy_sell


class Stock:

	def __init__(self, symbol, par_value, last_dividend):
		self.symbol = symbol
		self.par_value = par_value
		self.last_dividend = last_dividend
		self.trades = []

	def dividend_yield(self, price: float) -> float:
		raise NotImplementedError

	def pe_ratio(self, price) -> float:
		if self.last_dividend == 0.0:
			print(f"{self.symbol} : P/E_ratio cannot be calculated as dividend is 0")
			return 0.0
		return price / self.last_dividend

	def vwsp(self, seconds=-1) -> float:
		if len(self.trades) == 0:
			print(f"{self.symbol} : Volume weighted stock price cannot be calculated as there are no trades yet")
			return 0.0
		numerator = denominator = 0.0
		process_all_trades = True
		allowed_trade_time = datetime.datetime.now()
		if seconds > 0:
			process_all_trades = False
			allowed_trade_time -= datetime.timedelta(seconds=seconds)
		for trade in self.trades[::-1]:
			if not process_all_trades and trade.timestamp < allowed_trade_time:
				break
			numerator += trade.price * trade.quantity
			denominator += trade.quantity
		if denominator == 0.0:
			print(f"{self.symbol} : Volume weighted stock price cannot be calculated as there are no trades done in last {seconds}s")
			return 0.0
		return numerator / denominator

	def add_a_trade(self):
		q = int(input("Quantities : "))
		p = float(input("Price : "))
		bsc = input("Buy/Sell - Y/y for Buy, any other key for Sell : ")
		bs = BuySell.BUY if bsc in ['Y', 'y'] else BuySell.SELL
		self.trades.append(Trade(self.symbol, datetime.datetime.now(), q, p, bs))

	def analyse_stock(self):
		while True:
			print("\n------------------------------")
			print(f"\n       Analyse Stock ({self.symbol})")
			print("\n------------------------------")
			print("1.\tGet Dividend Yield")
			print("2.\tGet P/E Ratio")
			print("3.\tAdd a new trade")
			print("4.\tCalculate Volume Weighted Stock Price of last 5 minutes")
			print("5.\tExit from analysing this stock")
			ch = int(input("Enter your choice (a valid number) : "))
			if ch == 1:
				price = float(input("Enter Price : "))
				print(f"Dividend Yield : {self.dividend_yield(price)}")
			elif ch == 2:
				price = float(input("Enter Price : "))
				print(f"P/E Ratio : {self.pe_ratio(price)}")
			elif ch == 3:
				self.add_a_trade()
				print("Trade added")
			elif ch == 4:
				print(f"Volume Weighted Stock Price of last 5 minutes : {self.vwsp(seconds=300)}")
			elif ch == 5:
				break


class CommonSymbol(Stock):
	def dividend_yield(self, price: float) -> float:
		if price == 0.0:
			print(f"{self.symbol} : Common dividend yield cannot be calculated as price is 0")
			return 0.0
		return self.last_dividend / price


class PreferredSymbol(Stock):

	def __init__(self, fixed_dividend, *args, **kwargs):
		self.fixed_dividend = fixed_dividend / 100
		super(PreferredSymbol, self).__init__(*args, **kwargs)

	def dividend_yield(self, price: float) -> float:
		if price == 0.0:
			print(f"{self.symbol} : preferred dividend yield cannot be calculated as price is 0")
			return 0.0
		return (self.fixed_dividend * self.par_value) / price


class SuperSimpleStockMarket:

	def __init__(self):
		self.stocks = {}

	def gbce_all_share_index(self) -> float:
		if len(self.stocks) == 0:
			print("GBCE All Share Index cannot be calculated as there are no stocks yet in market")
			return 0.0
		share_index_value = 1
		for _, _stock in self.stocks.items():
			share_index_value *= _stock.vwsp()
		return pow(share_index_value, 1 / len(self.stocks))

	def analyse_market(self):
		stock_symbols = list(self.stocks.keys())
		while True:
			print("\n------------------------------")
			print(f"\n       Analyse Stock Market")
			print("\n------------------------------")
			print("1.\tGet GBCE All Share Index")
			print("2.\tAdd a new Symbol")
			for no, sym in enumerate(stock_symbols, 3):
				print(f"{no}.\tAnalyse Existing Symbol ({sym})")
			print(f"{len(self.stocks)+3}.\tExit")
			ch = int(input("Enter your choice (a valid number) : "))
			if ch == 1:
				print(f"GBCE All Share Index : {self.gbce_all_share_index()}")
			elif ch == 2:
				symbol = input("Enter Symbol : ")
				cps = input("Common/Preferred - Y/y for Common, any other key for Preferred: ")
				last_dividend = float(input("Last Dividend : "))
				par_value = float(input("Par Value : "))
				if cps in ['Y', 'y']:
					self.stocks[symbol] = CommonSymbol(symbol, par_value, last_dividend)
				else:
					fixed_dividend = float(input("Fixed Dividend : "))
					self.stocks[symbol] = PreferredSymbol(fixed_dividend, symbol, par_value, last_dividend)
				stock_symbols = list(self.stocks.keys())
			elif ch == len(self.stocks) + 3:
				break
			else:
				self.stocks[stock_symbols[ch - 3]].analyse_stock()


if __name__ == '__main__':
	sssm = SuperSimpleStockMarket()
	sssm.analyse_market()
