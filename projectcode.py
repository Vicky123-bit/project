import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load publicly available phishing email dataset
file_path = "CEAS_08.csv"  # Replace with actual dataset file

try:
    data = pd.read_csv(file_path)

    # Ensure dataset has the required columns
    if "content" not in data.columns or "label" not in data.columns:
        raise ValueError("Dataset must contain 'content' and 'label' columns")

    # Preprocessing: Handle missing values
    data.dropna(subset=["content", "label"], inplace=True)

    # Define input (X) and output labels (y)
    X = data["content"]  # Email text content
    y = data["label"].astype(int)  # 1 = phishing, 0 = legitimate

    # Convert email text into numerical features using TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)

    # Split dataset into training and testing sets (80-20 split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Transform text data into TF-IDF features
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train a Naïve Bayes model
    model = MultinomialNB(alpha=1.0)  # Laplace smoothing
    model.fit(X_train_tfidf, y_train)

    # Model evaluation
    y_pred = model.predict(X_test_tfidf)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Legitimate', 'Phishing'], yticklabels=['Legitimate', 'Phishing'])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix for Phishing Email Detection")
    plt.show()

    # Function to classify new emails
    def classify_email(email_text):
        email_tfidf = vectorizer.transform([email_text])
        prediction = model.predict(email_tfidf)
        return "Phishing" if prediction == 1 else "Legitimate"

    # Example classification
    test_email = "Your account has been locked due to suspicious activity. Click here to verify your identity."
    print("Test Email Classification:", classify_email(test_email))

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please check the file path.")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
