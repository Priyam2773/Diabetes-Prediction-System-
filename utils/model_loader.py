import os
import pickle
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

@st.cache_resource
def load_or_train_model():
    """Load pre-trained model or train & save if not exists."""
    model_path = "models/logistic_reg.sav"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model
    else:
        # Load dataset (using capitalization version compatible across platforms)
        df = pd.read_csv("Diabetes.csv")
        
        # Split inputs
        X = df.drop("Outcome", axis=1)
        y = df["Outcome"]
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Create pipeline with scaling and logistic regression
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42))
        ])
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        st.success(f"✅ Model trained on the fly. Test accuracy: {acc:.2f}")
        
        # Save model
        os.makedirs("models", exist_ok=True)
        with open(model_path, "wb") as f:
            pickle.dump(pipeline, f)
        return pipeline
