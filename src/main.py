import yfinance as yf
from GUI import onButton

# Default ticker is Apple
ticker = "SPY"
DateArray = yf.Ticker(ticker).options


def askForTicker():
    # Prompt the user for a new ticker
    global ticker
    ticker = onButton()
    print("Ticker was: " + ticker)


def getOptionsChain(inputString):
    # Retrieve the Options Chain Expiration dates from Yahoo Finance
    YFticker = yf.Ticker(inputString)
    global DateArray
    DateArray = YFticker.options


def displayOptionsChain():
    print("Length of the Chain: " + str(len(DateArray)) + "\n")
    print("\n".join(DateArray))


askForTicker()
getOptionsChain(ticker)
displayOptionsChain()
