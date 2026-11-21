# project
# Machine Learning Enhanced Phishing Email Detection

## Project Overview

This project explores the use of machine learning to identify phishing emails and distinguish them from legitimate emails.

The project compares two supervised machine-learning algorithms:

- Multinomial Naïve Bayes
- Random Forest Classifier

Email text is processed using Natural Language Processing (NLP) techniques and TF-IDF vectorisation. Both models are trained and evaluated to compare their phishing detection performance.

## Objectives

- Understand common phishing email threats and techniques.
- Develop machine-learning models to classify phishing and legitimate emails.
- Compare Naïve Bayes and Random Forest performance.
- Evaluate models using accuracy, precision, recall and confusion matrices.
- Explore improvements for future phishing detection systems.

## Technologies Used

- Python
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn
- TF-IDF Vectorisation
- Natural Language Processing (NLP)

## Dataset

The project uses a publicly available phishing email dataset from Kaggle, containing 11,229 email samples.

The dataset includes:
- Email body text
- Classification labels:
  - `1` – Phishing email
  - `0` – Legitimate email

The dataset is divided into 80% training data and 20% testing data.

Please refer to the original dataset source and its licence before redistributing any dataset files.

## Methodology

1. Load the phishing email dataset.
2. Handle missing values and prepare email text.
3. Convert email text into numerical features using TF-IDF.
4. Split the dataset into training and testing sets.
5. Train a Multinomial Naïve Bayes classifier.
6. Train a Random Forest classifier using 100 estimators.
7. Generate predictions and evaluate both models.
8. Compare the results using classification metrics and confusion matrices.

## Results

The results reported in the academic project were:

| Metric | Naïve Bayes | Random Forest |
|---|---:|---:|
| Accuracy | 98% | 99% |
| Precision | 97% | 99% |
| Recall | 97% | 99% |
| False Positives | 47 | 21 |
| False Negatives | 39 | 18 |

Random Forest performed better across the reported metrics, while Naïve Bayes offered a simpler and faster classification approach.

These are the results reported in the original project and should be reproducible against the same dataset and implementation before being treated as independently verified.

## Limitations and Future Improvements

Potential improvements include:

- Analysing email headers and sender information.
- Detecting suspicious URLs and spoofed domains.
- Exploring BERT and LSTM-based models.
- Developing a hybrid detection approach.
- Exploring integration with enterprise email security systems and SIEM platforms.

## Academic Project

MSc Cyber Security  
University of Hertfordshire  
2025

This repository presents an academic cybersecurity project on machine-learning-based phishing email detection.
