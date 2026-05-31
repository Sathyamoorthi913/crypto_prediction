import pandas as pd
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

print(" initalizing nlp lexions")
nltk.download('vader_lexicon',quiet=True)

def analyze_sentiment(news_path="data/raw_news.csv"):
    print(f"loading news data from{news_path}")
    if not os.path.exists(news_path):
        print(f"error: {news_path} not foound ")
        return None
    df=pd.read_csv(news_path)
    sia=SentimentIntensityAnalyzer()
    print("calulating sentiment scores for headlines")
    df['sentiment_score'] = df['headline'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
    
    print("aggregate sentiment scores by date")
    daily_sentiment =df.groupby('date')['sentiment_score'].mean().reset_index()

    return daily_sentiment
def merge_pipeline(price_path="data/raw_prices.csv",news_path="data/raw_news.csv"):
    if not os.path.exists(price_path):
        print(f"error: {price_path} not found")
        return
    price_df = pd.read_csv(price_path)
    if 'data' in price_df.columns:
        price_df=price_df.rename(columns={'data':'date'})
    sentiment_df=analyze_sentiment(news_path)
    if sentiment_df is None:
        return
    print("merging prices and sentiment data streams")
    price_df['date']=price_df['date'].astype(str)
    sentiment_df['date']=sentiment_df['date'].astype(str)
    final_df=pd.merge(price_df,sentiment_df,on='date',how='left')
    final_df['sentiment_score']=final_df['sentiment_score'].fillna(0)

    output_path="data/processed_data.csv"
    final_df.to_csv(output_path,index=False)
    print(f"feature matrix successfully saved'{output_path}':")

if __name__=="__main__":
    print("==starting data pipeline==")
    merge_pipeline()
    print("\n ===processing complete ===")
