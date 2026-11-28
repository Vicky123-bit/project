"""Phishing email detection with Multinomial Naive Bayes on TF-IDF features.

Usage:  python naive_bayes.py [path/to/CEAS_08.csv]
"""
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

DATA = sys.argv[1] if len(sys.argv) > 1 else "data/CEAS_08.csv"
os.makedirs("results", exist_ok=True)

data = pd.read_csv(DATA)
if "body" not in data.columns or "label" not in data.columns:
    raise ValueError("Dataset must contain 'body' (email text) and 'label' (1 = phishing, 0 = legitimate)")

X = data["body"].astype(str)
y = data["label"].astype(int)

# 80:20 split, fixed seed so results are reproducible
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_tfidf, y_train)
y_pred = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"], digits=4))

# A few classified test emails, for a quick sanity check
sample = X_test.to_frame("email").assign(actual=y_test.values, predicted=y_pred)
sample[["actual", "predicted"]] = sample[["actual", "predicted"]].replace({1: "Phishing", 0: "Legitimate"})
print(sample.head(10))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Legitimate", "Phishing"], yticklabels=["Legitimate", "Phishing"])
plt.title("Confusion Matrix (Naive Bayes)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("results/confusion_matrix_naive_bayes.png", dpi=120)
plt.show()
