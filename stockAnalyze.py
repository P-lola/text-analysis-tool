import yfinance as yf
from datetime import datetime

def extractBasicInfo(data):
  keysToExtract = ['longName','sector', 'website', 'fullTimeEmployees', 'marketCap', 'totalRevenue', 'trailingEPS']
  basicInfo = {}
  for key in keysToExtract:
    if key in data:
      basicInfo[key] = data[key]
    else:
      basicInfo[key] = ""
  return basicInfo

def getPriceHistory(company):
  companyHistory = company.history(period='12mo')
  prices = companyHistory['Open'].tolist()
  dates = companyHistory.index.strftime('%Y-%m-%d').tolist()
  return {
    'price': prices,
    'date': dates
  }

def getEarningsDates(company):
  earningDatesDF = company.earnings_dates
  allDates = earningDatesDF.index.strftime('%Y-%m-%d').tolist()
  date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in allDates]
  today = datetime.today()
  future_dates = [d.strftime('%Y-%m-%d') for d in date_objects if d > today]
  return future_dates

def getCompanyNews(company):
  newsList = company.news
  allNewsArticles = []
  for newsDict in newsList:
    newsDictToAdd = {
      'title': newsDict['content']['title'],
      'link': newsDict['content']['canonicalUrl']['url']
    }
    allNewsArticles.append(newsDictToAdd)
  return allNewsArticles

def getCompanyStockInfo(tickerSymbol):
  #GEt data from Yahoo Finance API
  company = yf.Ticker(tickerSymbol)

  #Get basic info on company
  basicInfo = extractBasicInfo(company.info)
  priceHistory = getPriceHistory(company)
  futureEarningsDates = getEarningsDates(company)
  newsArticles = getCompanyNews(company)


getCompanyStockInfo('MSFT')