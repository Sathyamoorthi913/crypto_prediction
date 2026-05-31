import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def load_and_engineer_features(file_path="data/processed_data.csv"):
    """
    Loads the processed CSV, creates ML features and labels,
    and handles shifting for next-day price prediction.
    """
    print(f"[*] Loading feature matrix from {file_path}...")
    if not os.path.exists(file_path):
        print(f"[X] Error: {file_path} not found. Run your processing script first!")
        return None, None
        
    df = pd.read_csv(file_path)
    
    # Sort by date to make sure time-series sequences are correct
    df = df.sort_values(by='date').reset_index(drop=True)
    
    print("[*] Engineering ML features...")
    # Feature 1: The percentage change of today's price compared to yesterday's
    df['price_pct_change'] = df['prices'].pct_change()
    
    # Target Label (y): Will tomorrow's price go UP (1) or DOWN (0)?
    # We shift the price column up by -1 to peek into the "tomorrow" value
    df['tomorrow_price'] = df['prices'].shift(-1)
    
    # If tomorrow's price is higher than today's price, assign 1, else 0
    df['target'] = (df['tomorrow_price'] > df['prices']).astype(int)
    
    # Drop rows with NaN values caused by pct_change (first row) and shift (last row)
    df = df.dropna().reset_index(drop=True)
    
    # Define our Feature columns (X) and Target column (y)
    feature_cols = ['prices', 'sentiment_score', 'price_pct_change']
    X = df[feature_cols]
    y = df['target']
    
    return X, y

def train_crypto_model():
    """Trains a Random Forest Classifier and prints evaluation metrics."""
    # 1. Prepare data
    X, y = load_and_engineer_features()
    if X is None or y is None:
        return
        
    print(f"[*] Dataset ready. Total samples: {len(X)}")
    
    # 2. Split into Train and Test sets (80% train, 20% test)
    # Note: We set shuffle=False because this is time-series data!
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    print(f"[*] Training Data Samples: {len(X_train)} | Testing Data Samples: {len(X_test)}")
    print("[*] Initializing and training Random Forest Classifier...")
    
    # 3. Initialize and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 4. Make predictions on the test set
    print("[*] Generating predictions on test data...")
    predictions = model.predict(X_test)
    
    # 5. Evaluate the results
    accuracy = accuracy_score(y_test, predictions)
    print("\n================ MODEL PERFORMANCE ================")
    print(f"Overall Model Accuracy: {accuracy:.2%}\n")
    print("Detailed Classification Report:")
    print(classification_report(y_test, predictions, target_names=['Price Down', 'Price Up']))
    print("====================================================")
    
    # Feature Importance display
    importances = model.feature_importances_
    print("\nFeature Importances:")
    for col, importance in zip(X.columns, importances):
        print(f" - {col}: {importance:.2%}")

if __name__ == "__main__":
    print("=== STARTING ML MODEL TRAINING PIPELINE (STEP 3) ===\n")
    train_crypto_model()
    print("\n=== TRAINING PROCESS COMPLETE ===")