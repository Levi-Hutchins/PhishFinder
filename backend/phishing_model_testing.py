# Just messing around with Sklearn before the notebook
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from config.paths_config import DATA

df = pd.read_csv(DATA)
def data_insights(df):
    print(df.head)
    print(df.columns)

#data_insights(df)

# These are the features I selected to be most important when identifying a phishing link
''' TODO: Revise these features during the learning process
    - Can i get the information 
'''
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

X = df[features]
Y = df["Result"]

X.drop_duplicates()
Y.drop_duplicates()

#print(X.shape)
#print(Y.shape)
def models():
    log_reg = LogisticRegression()
    log_reg.fit


X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.8, test_size=0.2, shuffle=True)

forest = RandomForestClassifier(max_depth=3, random_state=0)
log_reg = LogisticRegression()
forest.fit(X_train, y_train)
f_pred = forest.predict(X_test)
kn = KNeighborsClassifier(n_neighbors=20)

def find_n_neighbors():
    misclassified = []

    for i in range(1,20):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(X_train, y_train)
        pred_i = knn.predict(X_test)
        misclassified.append((y_test != pred_i).sum())


kn.fit(X_train, y_train)
pred_i = kn.predict(X_test)
print(kn.score(X_test,y_test))
print("Success")