import requests
import whois

import datetime
import html

import validators

import re
import bleach


from requests.exceptions import SSLError
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
    unvalidated_url = clean_url(url)

    if is_valid_url(unvalidated_url):

        try:
            if requests.get(url).ok: return 1
        except SSLError as e:
            return -1
        except Exception as e:
            return 0
    else:
        return 404
    
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



def is_valid_url(unvalidated_url: str) -> bool:
    contains_escapedChars = r'&[#]?[a-zA-Z0-9]+;'

    isvalid_1 = validators.url(unvalidated_url)
    isvalid_2 = re.search(contains_escapedChars, unvalidated_url)

    if isvalid_1 and isvalid_2 == None: return True
    else: return False


def clean_url(unclean_url: str) -> str:

    clean_layer_1 = bleach.clean(unclean_url)
    clean_layer_2 = html.escape(clean_layer_1)

    return clean_layer_2


def get_url_prediction_values(url_string: str):
    x_values = []
    unvalidated_url = clean_url(url_string)

    if is_valid_url(unvalidated_url):
        contains_ip = r'(?:\d{1,3}\.){3}\d{1,3}'
        x_values.append(-1) if re.search(contains_ip, unvalidated_url) else x_values.append(1)
        x_values.append(-1) if len(unvalidated_url) >= 54 else x_values.append(1)
    


        try: x_values.append(-1) if requests.head(unvalidated_url).status_code == 301 or requests.head(unvalidated_url).status_code == 302 else x_values.append(1)
        except requests.ConnectionError: 
            print("Issue Checking Link")
            x_values.append(-1)
        x_values.append(-1) if '@' in unvalidated_url else x_values.append(1)

        x_values.append(-1) if unvalidated_url.count("//") > 1 else x_values.append(1)
    
        x_values.append(verify_subdomains(unvalidated_url))

        x_values.append(verify_ssl(unvalidated_url))

        x_values.append(verify_domain_reglen(unvalidated_url))

        x_values.append(-1) if "https" in unvalidated_url and "https" != unvalidated_url[:5] else x_values.append(1)

        return x_values
    else: return 404



#print(get_url_prediction_values("http://httpsshorturl.at/bnsvZ"))
#print(verify_domain("stackoverflow.com"))
