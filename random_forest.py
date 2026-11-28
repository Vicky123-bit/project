"""Phishing email detection with a Random Forest on TF-IDF features (unigrams + bigrams).

Usage:  python random_forest.py [path/to/CEAS_08.csv]
"""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

DATA = sys.argv[1] if len(sys.argv) > 1 else "data/CEAS_08.csv"
os.makedirs("results", exist_ok=True)

data = pd.read_csv(DATA).rename(columns={"body": "content"})
if "content" not in data.columns or "label" not in data.columns:
    raise ValueError(f"Dataset must contain 'body' and 'label' columns, found: {list(data.columns)}")
data = data.dropna(subset=["content", "label"])

X = data["content"].astype(str)
y = data["label"].astype(int)  # 1 = phishing, 0 = legitimate

# Same 80:20 split and seed as naive_bayes.py, so both models see the same test emails
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_tfidf, y_train)
y_pred = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"], digits=4))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Legitimate", "Phishing"], yticklabels=["Legitimate", "Phishing"])
plt.title("Confusion Matrix (Random Forest)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("results/confusion_matrix_random_forest.png", dpi=120)
plt.show()

# Which words and phrases the forest relies on most
importances = model.feature_importances_
top = np.argsort(importances)[-20:]
features = vectorizer.get_feature_names_out()
plt.figure(figsize=(10, 6))
plt.title("Top 20 Important Features (Random Forest)")
plt.barh(range(len(top)), importances[top], align="center")
plt.yticks(range(len(top)), [features[i] for i in top])
plt.xlabel("Feature importance")
plt.tight_layout()
plt.savefig("results/top_features_random_forest.png", dpi=120)
plt.show()
