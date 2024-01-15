import requests
import whois
import datetime
from requests.exceptions import SSLError
import re
import whois
from urllib.parse import urlparse
'''
Requirements to make a prediction:
    "having_IPhaving_IP_Address", # URL contains IP - COMPLETE
    "URLURL_Length", # Length of the URL - COMPLETE
    "having_At_Symbol", # URL contains @ - COMPLETE
    "Shortining_Service", # Long URL shorted eg. bit.ly... - COMPLETE
    "double_slash_redirecting", # URL contains redirect to another site - COMPLETE
    "having_Sub_Domain", # www.aus.go.au - COMPLETE
    "SSLfinal_State", # URL uses HTTPS - COMPLETE
    "Domain_registeration_length", # URL domain is registed for short period - COMPLETE
    "HTTPS_token", # URL contains http://https - COMPLETE
    "Google_Index", # Can be find via google or not - TODO Dont know how at this stage dropping from model training
    "Page_Rank", # Measures how important a page is on the internet 0 or 1 - TODO Dont know how at this stage dropping from model training
    "port", # Scammers open all ports on there server to allow all services - TODO would like to figure out how to securely implement this
'''
def verify_ssl(url):
    try:
        if requests.get(url).ok: return 1
    except SSLError as e:
        return -1
    except Exception as e:
        return 0
    
def verify_domain_reglen(url):
    domain_data = whois.whois(url)
    
    creation_date = domain_data["creation_date"]
    expiration_date = domain_data["expiration_date"]
    # Some responses seem to come in lists
    if isinstance(creation_date, list): creation_date = creation_date[0]
    if isinstance(expiration_date, list): expiration_date = expiration_date[0]

    today = datetime.datetime.now()
    domain_age_days = (today - creation_date).days
    time_until_expiration_days = (expiration_date - today).days



    if domain_age_days > 365 and time_until_expiration_days > 365: return 1  

    elif domain_age_days < 365 and time_until_expiration_days < 365: return -1  

    else: return 0  


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

    x_values.append(verify_domain_reglen(url_string))

    x_values.append(-1) if "https" in url_string and "https" != url_string[:5] else x_values.append(1)

    return x_values



#print(get_url_prediction_values("http://httpsshorturl.at/bnsvZ"))
#print(verify_domain("stackoverflow.com"))

