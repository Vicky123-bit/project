import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load phishing email dataset
file_path = "/Users/vikram/Desktop/CEAS_08.csv"
data = pd.read_csv(file_path)

# Print dataset columns to verify
print("Dataset Columns:", data.columns.tolist())

# Use correct columns for email text and labels
if "body" not in data.columns or "label" not in data.columns:
    raise ValueError("Dataset must contain 'body' (email text) and 'label' (phishing indicator) columns")

# Assign email text and labels
X = data["body"]  # Email content
y = data["label"].astype(int)  # 1 = phishing, 0 = legitimate

# Convert email text into numerical features using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Naïve Bayes model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Evaluate model
y_pred = model.predict(X_test_tfidf)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Predict the labels for the test dataset
y_pred = model.predict(X_test_tfidf)

# Add predictions to the original test dataset for better visualization
test_results = X_test.to_frame()
test_results["Actual Label"] = y_test.values
test_results["Predicted Label"] = y_pred

# Convert 1 = "Phishing", 0 = "Legitimate"
test_results["Actual Label"] = test_results["Actual Label"].map({1: "Phishing", 0: "Legitimate"})
test_results["Predicted Label"] = test_results["Predicted Label"].map({1: "Phishing", 0: "Legitimate"})

# Display first 10 classified emails
print(test_results.head(100))

# Confusion Matrix for Naïve Bayes
cm_nb = confusion_matrix(y_test, y_pred)
sns.heatmap(cm_nb, annot=True, fmt='d', cmap='Blues', xticklabels=['Legitimate', 'Phishing'], yticklabels=['Legitimate', 'Phishing'])
plt.title("Naïve Bayes Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()