import pandas as pd
from config.paths_config import DATA

df = pd.read_csv(DATA)
def data_insights(df):
    print(df.head)
    print(df.columns)

data_insights(df)

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
print(X.columns)
print("Success")