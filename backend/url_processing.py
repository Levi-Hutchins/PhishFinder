import requests
from requests.exceptions import SSLError
import re
from urllib.parse import urlparse
'''
Requirements to make a prediction:
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
'''
def verify_ssl(url):
    try:
        if requests.get(url).ok: return 1
    except SSLError as e:
        return -1
    except Exception as e:
        return 0
    

def verify_subdomains(url):
    try:
        parsed_url = urlparse(url)
        subdomains = parsed_url.netloc.split('.')
        if len(subdomains) <= 3: return 1
        elif len(subdomains) > 3 and len(subdomains) <= 5: return 0
        elif len(subdomains) > 5: return -1

    except Exception as e: return 0

def get_url_prediction_values(url_string: str):
    x_values = []
    contains_ip = r'(?:\d{1,3}\.){3}\d{1,3}'
    x_values.append(-1) if re.search(contains_ip, url_string) else x_values.append(1)
    x_values.append(-1) if len(url_string) >= 54 else x_values.append(1)
    
    try: x_values.append(-1) if requests.head(url_string).status_code == 301 or requests.head(url_string).status_code == 302 else x_values.append(1)
    except requests.ConnectionError: 
        print("Issue Checking Link")
        x_values.append(-1)
    x_values.append(-1) if '@' in url_string else x_values.append(1)

    x_values.append(-1) if url_string.count("//") > 1 else x_values.append(1)
   
    x_values.append(verify_subdomains(url_string))

    x_values.append(verify_ssl(url_string))

    return x_values



print(get_url_prediction_values("https://shorturl.at/bnsvZ"))



