from mpl_toolkits.mplot3d import Axes3D
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
from GUI import *
import seaborn as sb
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import sys


# pre-set values
ticker = "AMD"
DateArray = yf.Ticker(ticker).options
strikeChoice = DateArray[2]
opt = yf.Ticker(ticker).option_chain(strikeChoice)
calls = opt.calls
puts = opt.puts
ArrayStore = None


def askForTicker():
    # Prompt the user for a new ticker
    global ticker, strikeChoice, opt
    ticker = onButton()
    print("Ticker was: " + ticker)
    # pickAStrike2()  # <---- causes ZSH error


def getOptionsChain(inputString):
    # Retrieve the Options Chain Expiration dates from Yahoo Finance
    YFticker = yf.Ticker(inputString)
    global DateArray
    tempTuple = ("Pick a Strike Price",)
    DateArray = tempTuple+YFticker.options


def pickAStrike():
    global strikeChoice, opt
    pickStrikePrice(DateArray)
    strikeChoice = returnChoice()
    opt = yf.Ticker(ticker).option_chain(strikeChoice)
    print("Strike Choice was: " + strikeChoice)


def pickAStrike2():
    global strikeChoice, opt
    strikeChoice = DateArray[2]
    opt = yf.Ticker(ticker).option_chain(strikeChoice)
    print("Strike Choice was: " + strikeChoice)


def sortCallsandPuts():
    global calls, puts, opt
    calls = opt.calls
    calls = cleaner(calls)
    calls['Mid Price'] = calls.apply(lambda row: (row.ask + row.bid)/2, axis=1)
    calls = calls.drop(columns=["ask", "bid"])
    calls = calls[["strike", "Mid Price", "openInterest", "volume"]]

    puts = opt.puts
    puts = cleaner(puts)
    puts['Mid Price'] = puts.apply(lambda row: (row.ask + row.bid)/2, axis=1)
    puts = puts.drop(columns=["ask", "bid"])
    puts = puts[["strike", "Mid Price", "openInterest", "volume"]]


def cleaner(object):
    return object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice",
                                "change", "percentChange", "impliedVolatility", "inTheMoney", "contractSize", "currency"])


def heatCleaner(object):
    object = object.drop(columns=["contractSymbol", "lastTradeDate", "lastPrice",
                                  "change", "percentChange", "volume", "inTheMoney", "contractSize", "currency", "impliedVolatility", "ask", "bid"])
    object = object[["strike", "openInterest"]]
    return object


def heatCleanerVOLUME(object):
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


def displayOptionsChain():
    print("Length of the Chain: " + str(len(DateArray)) + "\n")
    print("\n".join(DateArray))


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
    sortCallsandPuts()
    callData = calls.drop(columns=['Mid Price', 'volume'])
    putData = puts.drop(columns=['Mid Price', 'volume'])
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
    plt.clf()
    img = Image.open('out.png')
    img.show()
    # plt.show(block=True)
    print("***********************")

# dataframe place NaN with 0


def CallsOIMap():  # plt.style.use("dark_background")
    callsArray = heatCleaner(opt.calls)
    callsArray.rename(columns={'openInterest': DateArray[1]}, inplace=True)
    for x in range(2, len(DateArray)-1):
        opt2 = yf.Ticker(ticker).option_chain(DateArray[x])
        callsArray2 = heatCleaner(opt2.calls)
        callsArray2.rename(
            columns={'openInterest': DateArray[x]}, inplace=True)
        callsArray = pd.merge(callsArray, callsArray2, on='strike')
    callsArray.set_index('strike', inplace=True)
    callsArray = callsArray.fillna(0)
    print(callsArray)
    heat_map = sb.heatmap(callsArray, cmap="Reds", linewidths=0)
    global ArrayStore
    ArrayStore = callsArray
    plt.yticks(rotation=0)
    plt.xticks(rotation=50)
    plt.gca().invert_yaxis()
    plt.show()
    plt.clf()


def PutsOIMap():  # plt.style.use("dark_background")
    callsArray = heatCleaner(opt.puts)
    callsArray.rename(columns={'openInterest': DateArray[1]}, inplace=True)
    for x in range(2, len(DateArray)-1):
        opt2 = yf.Ticker(ticker).option_chain(DateArray[x])
        callsArray2 = heatCleaner(opt2.puts)
        callsArray2.rename(
            columns={'openInterest': DateArray[x]}, inplace=True)
        callsArray = pd.merge(callsArray, callsArray2, on='strike')
    callsArray.set_index('strike', inplace=True)
    callsArray = callsArray.fillna(0)
    print(callsArray)
    heat_map = sb.heatmap(callsArray, cmap="Blues", linewidths=0)
    global ArrayStore
    ArrayStore = callsArray
    plt.yticks(rotation=0)
    plt.xticks(rotation=50)
    plt.gca().invert_yaxis()
    plt.show()
    plt.clf()


def CallsVolumeMap():
    callsArray = heatCleanerVOLUME(opt.calls)
    callsArray.rename(columns={'volume': DateArray[1]}, inplace=True)
    for x in range(2, len(DateArray)-1):
        opt2 = yf.Ticker(ticker).option_chain(DateArray[x])
        callsArray2 = heatCleanerVOLUME(opt2.calls)
        callsArray2.rename(
            columns={'volume': DateArray[x]}, inplace=True)
        callsArray = pd.merge(callsArray, callsArray2, on='strike')
    callsArray.set_index('strike', inplace=True)
    callsArray = callsArray.fillna(0)
    print(callsArray)
    heat_map = sb.heatmap(callsArray, cmap="Reds", linewidths=0)
    global ArrayStore
    ArrayStore = callsArray
    plt.yticks(rotation=0)
    plt.xticks(rotation=50)
    plt.gca().invert_yaxis()
    plt.show()
    plt.clf()


def PutsVolumeMap():
    callsArray = heatCleanerVOLUME(opt.puts)
    callsArray.rename(columns={'volume': DateArray[1]}, inplace=True)
    for x in range(2, len(DateArray)-1):
        opt2 = yf.Ticker(ticker).option_chain(DateArray[x])
        callsArray2 = heatCleanerVOLUME(opt2.puts)
        callsArray2.rename(
            columns={'volume': DateArray[x]}, inplace=True)
        callsArray = pd.merge(callsArray, callsArray2, on='strike')
    callsArray.set_index('strike', inplace=True)
    callsArray = callsArray.fillna(0)
    print(callsArray)
    heat_map = sb.heatmap(callsArray, cmap="Blues", linewidths=0)
    global ArrayStore
    ArrayStore = callsArray
    plt.yticks(rotation=0)
    plt.xticks(rotation=50)
    plt.gca().invert_yaxis()
    plt.show()
    plt.clf()


def threedeegraph(object):

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
    ax.set_zlabel('Open Interest / Volume')
    # fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5)
    plt.show()
    plt.clf()


def askForStrikePrice():
    pickStrikePrice(calls['strike'].astype(str).tolist())


def setticker():
    askForTicker()
    getOptionsChain(ticker)


def optionchainMENU():
    sortCallsandPuts()
    displayOptionsChain()


def callOI3dmenu():
    CallsOIMap()
    threedeegraph(ArrayStore)


def putOI3dmenu():
    PutsOIMap()
    threedeegraph(ArrayStore)


def callVolumemenu():
    CallsVolumeMap()
    threedeegraph(ArrayStore)


def putVolumemenu():
    PutsVolumeMap()
    threedeegraph(ArrayStore)


def askForTickerMENU():
    askForTicker()
    getOptionsChain(ticker)
    pickAStrike2()


def mainMENUswitch():
    def switchBoard(arguement):
        switcher = {
            "setTicker": lambda: askForTickerMENU(),
            "setStrike": lambda: pickAStrike(),
            "optionChain": lambda: optionchainMENU(),
            "OImage": lambda: OIChart(),
            "CallVolumeMap": lambda: CallsVolumeMap(),
            "CallOIMap": lambda: CallsOIMap(),
            "PutVolumeMap": lambda: PutsVolumeMap(),
            "PutsOIMap": lambda: PutsOIMap(),
            "CallVolume3D": lambda: callVolumemenu(),
            "CallOI3D": lambda: callOI3dmenu(),
            "PutVolume3D": lambda: putVolumemenu(),
            "PutOI3D": lambda: putOI3dmenu(),
            "exit": lambda: sys.exit,
        }
        return switcher.get(arguement, lambda: "error")()

    print("******* \n Welcome to Sam's Option Scanner \n *******")
    while(True):
        print("PICK ONE: setticker, setstrike, optionchain, OIimage, CallVolumeMap, CallOIMap, PutVolumeMap, PutOIMap, CallVolume3D, CallOI3D, PutVolume3D, PutOI3D, exit")
        choice = input()
        switchBoard(choice)()


def mainMENUnested():
    def repeat():
        print("PICK ONE: setticker, setstrike, optionchain, OIimage, CallsVolumeMap, CallsOIMap, PutsVolumeMap, PutsOIMap, CallVolume3D, CallOI3D, PutVolume3D, PutOI3D, exit")
        choice = input()

        if choice == "setticker":
            # askForTicker()  # get ticker of choice from user
            # getOptionsChain(ticker)  # get entire option chain from yFinance
            askForTickerMENU()
            repeat()
        elif choice == "setstrike":
            pickAStrike()  # asks user for specific date
            # askForStrikePrice()  # prompts user to choose a strike from the table
            # displayOptionsChain() #show entire option chain
            repeat()
        elif choice == "optionchain":
            sortCallsandPuts()  # breaks options chain into essential data and sorts by calls / puts
            displayCleanOptionChain()  # displays calls and puts as a clean table
            repeat()
        elif choice == "OIimage":
            OIChart()
            repeat()
        elif choice == "CallsVolumeMap":
            CallsVolumeMap()
            repeat()
        elif choice == "CallsOIMap":
            CallsOIMap()
            repeat()
        elif choice == "PutsVolumeMap":
            PutsVolumeMap()
            repeat()
        elif choice == "PutsOIMap":
            PutsOIMap()
            repeat()
        elif choice == "CallVolume3D":
            CallsVolumeMap()
            threedeegraph(ArrayStore)
            repeat()
        elif choice == "CallOI3D":
            CallsOIMap()
            threedeegraph(ArrayStore)
            repeat()
        elif choice == "PutVolume3D":
            PutsVolumeMap()
            threedeegraph(ArrayStore)
            repeat()
        elif choice == "PutOI3D":
            PutsOIMap()
            threedeegraph(ArrayStore)
            repeat()
        elif choice == "exit":
            sys.exit()
        else:
            print("unexpected choice")
            repeat()

    print("******* \n Welcome to Sam's Option Scanner \n *******")
    repeat()


# mainMENUswitch()
mainMENUnested()
print("All done")
