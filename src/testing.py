import yfinance as yf

options = yf.Ticker("AMD").options
chain = yf.Ticker("AMD").option_chain(options[1]).calls
chain = chain.drop(columns=['contractSymbol', 'lastTradeDate', 'lastPrice', 'bid',
                            'ask', 'change', 'impliedVolatility', 'inTheMoney', 'contractSize', 'currency', 'percentChange'])
print(chain)
