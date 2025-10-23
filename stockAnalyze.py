import json
import yfinance as yf
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import analyze

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

def extractNewsArticleTextFromHtml(soup):
  allText = ""
  result =(soup.find_all("div", {"class":"body yf-h0on0w"}) + soup.find_all("article", {"id": "article-main-content", "class": "flex flex-col"}))
  for res in result:
    allText += res.text
  return allText


headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
}

def extractCompanyNewsArticles(newsArticles):
  allArticleText = ""
  for newsArticle in newsArticles:
    url = newsArticle['link']
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    if soup.find_all(string="Continue Reading"):
      print('Tag found - should skip')
    else:
      print("Tag not found, don't skip")
      allArticleText = extractNewsArticleTextFromHtml(soup)
    return allArticleText

def getCompanyStockInfo(tickerSymbol):
  #GEt data from Yahoo Finance API
  company = yf.Ticker(tickerSymbol)

  #Get basic info on company
  basicInfo = extractBasicInfo(company.info)
  priceHistory = getPriceHistory(company)
  futureEarningsDates = getEarningsDates(company)
  newsArticles = getCompanyNews(company)
  newsArticlesAllText = extractCompanyNewsArticles(newsArticles)
  newsTextAnalysis = analyze.analyzeText(newsArticlesAllText)

  finalStockAnalysis = {
    "basicInfo": basicInfo,
    "priceHistory": priceHistory,
    "futureEarningsDates": futureEarningsDates,
    "newsArticles": newsArticles,
    "newsTextAnalysis": newsTextAnalysis
  }
  return finalStockAnalysis


companySTockAnalysis = getCompanyStockInfo('MSFT')
print(json.dumps(companySTockAnalysis, indent=4))