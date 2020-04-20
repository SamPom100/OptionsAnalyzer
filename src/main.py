from mpl_toolkits.mplot3d import Axes3D
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
from GUI import *
from scrolly import *
import seaborn as sb
from mpl_toolkits.mplot3d import axes3d
import numpy as np

# Default ticker is Apple
ticker = "AMD"
DateArray = yf.Ticker(ticker).options
strikeChoice, opt, calls, puts, callsArrayStore = None, None, None, None, None


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


def pickAStrike2():
    global strikeChoice, opt
    strikeChoice = DateArray[1]
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


def OICleaner(object):
    object = object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice",
                                  "change", "percentChange", "volume", "inTheMoney", "contractSize", "currency", "impliedVolatility", "ask", "bid"])
    object = object[["strike", "openInterest"]]
    return object


def VolumeCleaner(object):
    object = object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice",
                                  "change", "percentChange", "openInterest", "inTheMoney", "contractSize", "currency", "impliedVolatility", "ask", "bid"])
    object = object[["strike", "volume"]]
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


def OpenInterestChart():
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
    fig = plt.figure()
    plt.show(block=True)
    # plt.savefig("out.png")
    #img = Image.open('out.png')
    # img.show()
    print("***********************")


def OIHeatMap():
    callsArray = OICleaner(opt.calls)
    callsArray.rename(columns={'volume': DateArray[1]}, inplace=True)
    for x in range(2, len(DateArray)-1):
        opt2 = yf.Ticker(ticker).option_chain(DateArray[x])
        callsArray2 = OICleaner(opt2.calls)
        callsArray2.rename(
            columns={'volume': DateArray[x]}, inplace=True)
        callsArray = pd.merge(callsArray, callsArray2, on='strike')
    callsArray.set_index('strike', inplace=True)

    print(callsArray)
    # plt.style.use("dark_background")
    heat_map = sb.heatmap(callsArray, cmap="Reds", linewidths=0)

    global callsArrayStore
    callsArrayStore = callsArray
    plt.yticks(rotation=0)
    plt.xticks(rotation=50)
    plt.gca().invert_yaxis()
    plt.title("Volume for all options of " + ticker + " per strike")
    plt.show()
    threedeegraph(callsArrayStore)


def VolumeHeatMap():
    callsArray = VolumeCleaner(opt.calls)
    callsArray.rename(columns={'openInterest': DateArray[1]}, inplace=True)
    for x in range(2, len(DateArray)-1):
        opt2 = yf.Ticker(ticker).option_chain(DateArray[x])
        callsArray2 = VolumeCleaner(opt2.calls)
        callsArray2.rename(
            columns={'openInterest': DateArray[x]}, inplace=True)
        callsArray = pd.merge(callsArray, callsArray2, on='strike')

    callsArray.set_index('strike', inplace=True)

    print(callsArray)
    # plt.style.use("dark_background")
    heat_map = sb.heatmap(callsArray, cmap="Reds", linewidths=0)

    global callsArrayStore
    callsArrayStore = callsArray
    plt.yticks(rotation=0)
    plt.xticks(rotation=90)
    plt.gca().invert_yaxis()
    plt.title("Volume for all options of " + ticker + " per strike")
    plt.show()
    threedeegraph(callsArrayStore)


def threedeegraph(object):

    plt.xticks(rotation=0)
    eg = object

    # thickness of the bars
    dx, dy = .8, .8

    # prepare 3d axes
    fig = plt.figure(figsize=(10, 6))
    ax = Axes3D(fig)

    # set up positions for the bars
    xpos = np.arange(eg.shape[0])
    ypos = np.arange(eg.shape[1])

    # set the ticks in the middle of the bars
    ax.set_xticks(xpos + dx/2)
    ax.set_yticks(ypos + dy/2)

    # create meshgrid
    # print xpos before and after this block if not clear
    xpos, ypos = np.meshgrid(xpos, ypos)
    xpos = xpos.flatten()
    ypos = ypos.flatten()

    # the bars starts from 0 attitude
    zpos = np.zeros(eg.shape).flatten()

    # the bars' heights
    dz = eg.values.ravel()

    # plot and color
    values = np.linspace(0.2, 1., xpos.ravel().shape[0])
    colors = cm.rainbow(values)
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors)

    # put the column / index labels
    ax.w_yaxis.set_ticklabels(eg.columns)
    ax.w_xaxis.set_ticklabels(eg.index)

    # name the axes
    ax.set_xlabel('Strike')
    # ax.set_ylabel('Date')
    ax.set_zlabel('Open Interest')
    ax.set_title('Open Interest 3D Bar Graph')
    #fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5)

    plt.show()


def askForStrikePrice():
    pickStrikePrice(calls['strike'].astype(str).tolist())


askForTicker()  # get ticker of choice from user
getOptionsChain(ticker)  # get entire option chain from yFinance
# displayOptionsChain() #show entire option chain
pickAStrike2()  # asks user for specific date
sortCallsandPuts()  # breaks options chain into essential data and sorts by calls / puts
# displays calls and puts at once as a merged and cleaned table
# displayCleanOptionChain()
# OpenInterestChart()

VolumeHeatMap()
# OIHeatMap()

# threedeegraph(callsArrayStore)


# askForStrikePrice()  # prompts user to choose a strike from the table


print("All done")
