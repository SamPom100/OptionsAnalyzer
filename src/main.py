import yfinance as yf
from GUI import onButton

# Default ticker is Apple
ticker = "AAPL"


def askForTicker():
    # Prompt the user for a new ticker
    ticker = onButton()
    print("Ticker was: " + ticker)


def getOptionsChain(inputString):
    # Retrieve the Options Chain Expiration dates from Yahoo Finance
    YFticker = yf.Ticker(inputString)
    DateArray = YFticker.options
    print("\n".join(DateArray))


askForTicker()
getOptionsChain(ticker)
