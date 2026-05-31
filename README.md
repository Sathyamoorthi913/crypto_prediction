# Crypto Sentiment & Price Prediction Pipeline

An end-to-end machine learning pipeline that collects live cryptocurrency data, evaluates market sentiment using Natural Language Processing (NLP), and attempts to predict next-day price movements.

## 🛠️ Tech Stack
* **Data Collection:** Python, Requests, CoinGecko API, NewsAPI
* **Data Engineering:** Pandas, NumPy
* **NLP (Sentiment Analysis):** NLTK (VADER Lexicon)
* **Machine Learning:** Scikit-Learn (Random Forest Classifier)

## 🏗️ Architecture Pipeline
1. `data_collection.py`: Hits CoinGecko for 30-day OHLCV data and NewsAPI for real-time market headlines.
2. `data_processing.py`: Normalizes data frames, tracks headline sentiments from -1 to +1, averages sentiment by date, and joins features into a master matrix.
3. `model_training.py`: Engineers target labels ($1$ for Up, $0$ for Down) shifted by $t+1$, splits time-series splits sequentially, trains a Random Forest Classifier, and evaluates metrics.

## 📊 Performance & Key Takeaways
On the initial baseline run with a limited 30-day evaluation window:
* **Baseline Accuracy:** ~33% 
* **Insight:** Financial markets are highly regime-dependent. The model showed an engineering bias toward predicting upward trajectories given the short testing horizon.
* **Feature Importance:** Price trends and percentage changes heavily out-weighted textual features due to API limits on historical news backtesting.

## 🚀 Future Cloud Extensions (AWS)
To move this production-grade pipeline completely to the cloud:
* Host the ingestion script on an **AWS EC2** instance or an **AWS Lambda** microservice.
* Schedule daily data execution cron-jobs using **Amazon CloudWatch**.
* Store structural streaming histories long-term inside an **AWS S3** data lake to steadily scale training samples out past 30 days.