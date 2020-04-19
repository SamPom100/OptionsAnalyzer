import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from GUI import *
from scrolly import *
import seaborn as sb

# Default ticker is Apple
ticker = "AMD"
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
    calls = cleaner(calls)
    calls['Mid Price'] = calls.apply(lambda row: (row.ask + row.bid)/2, axis=1)
    calls = calls.drop(columns=["ask", "bid"])
    calls = calls[["strike", "Mid Price", "openInterest", "impliedVolatility"]]

    puts = opt.puts
    puts = cleaner(puts)
    puts['Mid Price'] = puts.apply(lambda row: (row.ask + row.bid)/2, axis=1)
    puts = puts.drop(columns=["ask", "bid"])
    puts = puts[["strike", "Mid Price", "openInterest", "impliedVolatility"]]


def cleaner(object):
    return object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice",
                                "change", "percentChange", "volume", "inTheMoney", "contractSize", "currency"])


def heatCleaner(object):
    object = object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice",
                                  "change", "percentChange", "volume", "inTheMoney", "contractSize", "currency", "impliedVolatility", "ask", "bid"])
    object = object[["strike", "openInterest"]]
    return object


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
    # finalFrame = pd.concat([finalFrame, tempFrame])
    finalFrame = pd.merge(finalFrame, tempFrame, on='strike')
    finalFrame.plot.bar(figsize=(20, 8), x="strike", y=["Calls", "Puts"],
                        title="Open Interest for "+ticker.upper()+" all options at every strike on "+strikeChoice)

    ####################
    # fig = plt.figure()
    # a = ScrollableWindow(fig)
    plt.savefig("out.png")
    img = Image.open('out.png')
    img.show()
    # plt.show(block=True)
    print("***********************")

# dataframe place NaN with 0


def HeatMap():
    callsArray = heatCleaner(opt.calls)
    callsArray.rename(columns={'openInterest': DateArray[1]}, inplace=True)
    for x in range(2, len(DateArray)-1):
        opt2 = yf.Ticker(ticker).option_chain(DateArray[x])
        callsArray2 = heatCleaner(opt2.calls)
        callsArray2.rename(
            columns={'openInterest': DateArray[x]}, inplace=True)
        callsArray = pd.merge(callsArray, callsArray2, on='strike')
    #

    callsArray.set_index('strike', inplace=True)

    print(callsArray)
    heat_map = sb.heatmap(callsArray, cmap="Blues", linewidths=.7)
    plt.yticks(rotation=0)
    plt.xticks(rotation=70)
    plt.gca().invert_yaxis()
    plt.show()


def askForStrikePrice():
    pickStrikePrice(calls['strike'].astype(str).tolist())


askForTicker()  # get ticker of choice from user
getOptionsChain(ticker)  # get entire option chain from yFinance
# displayOptionsChain() #show entire option chain
pickAStrike()  # asks user for specific date
sortCallsandPuts()  # breaks options chain into essential data and sorts by calls / puts
# displays calls and puts at once as a merged and cleaned table
displayCleanOptionChain()
# OIChart()

HeatMap()


# askForStrikePrice()  # prompts user to choose a strike from the table


print("All done")
