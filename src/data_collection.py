import os
import requests
import pandas as pd
from datetime import datetime

coin="bitcoin"
currency="usd"
days="30"

news_api_key="43cbe04171dd4da99257beb6dbc2805c"

def fetch_crypto_prices(coin=coin ,vs_currency=currency,days=days):
    print(f"fetching the price data{coin}...")
    url=f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30"
    params={
        'vs_currency':vs_currency,
        'days':days,
        'interval':'daily'
    }
    try:
      response=requests.get(url,params=params)
      if response.status_code == 200:
        data=response.json()
        prices=data['prices']

        df=pd.DataFrame(prices,columns=['timestamp','prices'])
        df['data']=pd.to_datetime(df['timestamp'],unit='ms').dt.date
        df=df.drop(columns=['timestamp'])
        return df
      else:
        print(f"error fetcing data{response.status_code}")
        return None
    except Exception as e:
       print(f"[x] an exception occured whilefetching {e}")
       return None
    
    
def fetch_crypto_news(query=coin,api_key=news_api_key):
    print(f"fetching recent news from{query}")
    if not api_key: 
     print(f"[x]error: please provide a valid news api key")
     return None
    url="https://newsapi.org/v2/everything"
    params={
       'q':query,
       'language':'en',
       'sortBy':'publishedAt',
       'pageSize':100,
       'apikey':api_key
    }    
    try:
       response = requests.get(url,params=params)
       if response.status_code == 200:
          articles =response.json().get('articles',[])

          news_list=[]
          for article in articles:
             date_str=article['publishedAt'][:10]
             headline = article['title']
             news_list.append([date_str,headline])
          df = pd.DataFrame(news_list,columns=['date','headline'])
          df['date']=pd.to_datetime(df['date']).dt.date
          print(f"successfully fetched{len(df)}news headline")
          return df
       else:
          print(f"[x] error fetching news : HTTP status {response.status_code}")
          print(f"details: {response.json().get('message','no details provided')}")
          return None
    except Exception as e:
       print(f"[x] an error occured while fetching data {e}")
       return None
       
if __name__=="__main__":
   print("=== start crypto data pipeline ===\n")
   os.makedirs("data",exist_ok=True)

   price_df=fetch_crypto_prices()
   print("-"*50)
   news_df = fetch_crypto_news()
   print("-"*50)

   if price_df is not None and not price_df.empty:
      price_filepath="data/raw_prices.csv"
      price_df.to_csv(price_filepath,index=False)
      print(f"price data saved '{price_filepath}':")
      print(price_df.head(3))

   else:
      print("[x] failed to save thye data")

   print("-"*50)

   if news_df is not None and not news_df.empty:
      news_filepath = "data/raw_news.csv"
      news_df.to_csv(news_filepath,index=False)
      print(f"news data saved '{news_filepath}':")
      print(news_df.head(3))
   else:
      print(" failed to save the news data")
   print("\n ==finished==")

    