import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from config.paths_config import DATA
import random as r
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_csv(DATA)

# These are the features I selected to be most important when identifying a phishing link
features = [
    "having_IPhaving_IP_Address", # URL contains IP
    "URLURL_Length", # Length of the URL
    "having_At_Symbol", # URL contains @
    "Shortining_Service", # Long URL shorted eg. bit.ly...
    "double_slash_redirecting", # URL contains redirect to another site
    "having_Sub_Domain", # www.aus.go.au
    "SSLfinal_State", # URL uses HTTPS
    "Domain_registeration_length", # URL domain is registed for short period 
    "HTTPS_token", # URL contains http://https
    "Google_Index", # Can be find via google or not
    "Page_Rank", # Measures how important a page is on the internet 0 or 1
    "port", # Scammers open all ports on there server to allow all services
    "Favicon", # If the favicon is loaded from a domain other than that shown in the address bar - phish
    "Abnormal_URL", # Fetch by WHOIS database - API
    "age_of_domain", # Check current domain age
    "DNSRecord"
    ]

df.dropna(inplace=True)



X = df[features]
Y = df["Result"]

X.drop_duplicates()
Y.drop_duplicates()

X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.8, test_size=0.2, shuffle=True)

# Allow me to determine the best K neighbours required
def find_n_neighbors():
    misclassified = []

    for i in range(1,20):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(X_train, y_train)
        pred_i = knn.predict(X_test)
        misclassified.append((y_test != pred_i).sum())

knn_classifier = KNeighborsClassifier(n_neighbors=20)


knn_classifier.fit(X_train, y_train)
y_pred = knn_classifier.predict(X_test)

# Stats
print("---------- Model Statistics ----------\n")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='macro'))
print("Recall:", recall_score(y_test, y_pred, average='macro'))
print("F1 Score:", f1_score(y_test, y_pred, average='macro'))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n--------------------------------------")