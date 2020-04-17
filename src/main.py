import yfinance as yf
from GUI import *

# Default ticker is Apple
ticker = "AAPL"
DateArray = yf.Ticker(ticker).options
strikeChoice = None


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


def pickAStrike():
    global strikeChoice
    pickStrikePrice(DateArray)
    strikeChoice = returnChoice()
    print("Strike Choice was: " + strikeChoice)


askForTicker()
getOptionsChain(ticker)
displayOptionsChain()
pickAStrike()

print("All done")
