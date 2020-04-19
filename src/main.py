import yfinance as yf
#import tabulate as tabulate
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from GUI import *

# Default ticker is Apple
ticker = "AAPL"
DateArray = yf.Ticker(ticker).options
strikeChoice = None
opt = None
calls = None
puts = None


def askForTicker():
    # Prompt the user for a new ticker
    global ticker
    ticker = onButton()
    print("Ticker was: " + ticker)


def getOptionsChain(inputString):
    # Retrieve the Options Chain Expiration dates from Yahoo Finance
    YFticker = yf.Ticker(inputString)
    global DateArray
    tempTuple = ("Pick a Strike Price",)
    DateArray = tempTuple+YFticker.options


def displayOptionsChain():
    print("Length of the Chain: " + str(len(DateArray)) + "\n")
    print("\n".join(DateArray))


def pickAStrike():
    global strikeChoice, opt
    pickStrikePrice(DateArray)
    strikeChoice = returnChoice()
    opt = yf.Ticker(ticker).option_chain(strikeChoice)
    print("Strike Choice was: " + strikeChoice)


def sortCallsandPuts():
    global calls, puts, opt
    calls = opt.calls
    calls = calls.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice",
                                "change", "percentChange", "volume", "inTheMoney", "contractSize", "currency"])
    calls['Mid Price'] = calls.apply(lambda row: (row.ask + row.bid)/2, axis=1)
    calls = calls.drop(columns=["ask", "bid"])
    calls = calls[["strike", "Mid Price", "openInterest", "impliedVolatility"]]

    puts = opt.puts
    puts = puts.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice",
                              "change", "percentChange", "volume", "inTheMoney", "contractSize", "currency"])
    puts['Mid Price'] = puts.apply(lambda row: (row.ask + row.bid)/2, axis=1)
    puts = puts.drop(columns=["ask", "bid"])
    puts = puts[["strike", "Mid Price", "openInterest", "impliedVolatility"]]


def getCalls():
    print("****************** Calls *********************")
    print(calls)


def getPuts():
    print("****************** Puts *********************")
    print(puts)


def displayCleanOptionChain():
    print("****************** Calls **********************    ---[" + ticker.upper(
    )+"]---    ******************** Puts ********************* ")
    temp = {'             ': [""]}
    tempPD = pd.DataFrame(data=temp)
    merged = pd.concat([calls, tempPD, puts], axis=1)
    merged = merged.fillna("")
    # merged.style.hide_index()
    print(merged.to_string(index=False))
    ############


def OIChart():
    callData = calls.drop(columns=['Mid Price', 'impliedVolatility'])
    putData = puts.drop(columns=['Mid Price', 'impliedVolatility'])
    finalFrame = pd.DataFrame(callData)
    finalFrame.rename(columns={'openInterest': 'Calls'}, inplace=True)
    tempFrame = pd.DataFrame(putData)

    tempFrame.rename(columns={'openInterest': 'Puts'}, inplace=True)
    #finalFrame = pd.concat([finalFrame, tempFrame])
    finalFrame = pd.merge(finalFrame, tempFrame, on='strike')
    finalFrame.plot.bar(x="strike", y=["Calls", "Puts"],
                        title="Open Interest for "+ticker.upper()+" all options at every strike on "+strikeChoice)

    ####################

    plt.show(block=True)

    print("***********************")


def askForStrikePrice():
    pickStrikePrice(calls['strike'].astype(str).tolist())


askForTicker()  # get ticker of choice from user
getOptionsChain(ticker)  # get entire option chain from yFinance
# displayOptionsChain() #show entire option chain
pickAStrike()  # asks user for specific date
sortCallsandPuts()  # breaks options chain into essential data and sorts by calls / puts
# displays calls and puts at once as a merged and cleaned table
displayCleanOptionChain()
OIChart()

# askForStrikePrice()  # prompts user to choose a strike from the table


print("All done")
