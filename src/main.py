import yfinance as yf
from GUI import onButton
from GUI import pickStrikePrice
from GUI import returnChoice

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
    strikeChoice = pickStrikePrice(DateArray)
    print("Strike Choice was:" + returnChoice())


askForTicker()
getOptionsChain(ticker)
displayOptionsChain()
pickAStrike()


print("All done")
