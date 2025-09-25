import yfinance as yf

def extractBasicInfo(data):
  keysToExtract = ['longName','sector', 'website', 'fullTimeEmployees', 'marketCap', 'totalRevenue', 'trailingEPS']
  basicInfo = {}
  for key in keysToExtract:
    if key in data:
      basicInfo[key] = data[key]
    else:
      basicInfo[key] = ""
  return basicInfo

def getCompanyStockInfo(tickerSymbol):
  company = yf.Ticker(tickerSymbol)
  basicInfo = extractBasicInfo(company.info)
  print(basicInfo)

getCompanyStockInfo("MSFT")