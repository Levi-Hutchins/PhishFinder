import requests

import html
import bleach
import whois

from urllib.parse import urlparse
from validators import url as url_validator

import datetime
import re

import sys

sys.dont_write_bytecode = True

def clean_url(unclean_url: str) -> str:

    clean_layer_1 = bleach.clean(unclean_url)
    clean_layer_2 = html.escape(clean_layer_1)

    return clean_layer_2


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and url_validator(url)
    except:
        return False

def has_ip_address(url):
    return 1 if re.search(r'(?:\d{1,3}\.){3}\d{1,3}', url) else -1

def url_length(url):
    return -1 if len(url) >= 54 else 1

def has_at_symbol(url):
    return -1 if "@" in url else 1

def is_shortening_service(url):
    shortening_services = ['bit.ly', 'tinyurl.com', 'goo.gl']
    domain = urlparse(url).netloc
    return -1 if any(service in domain for service in shortening_services) else 1

def double_slash_redirecting(url):
    # After the protocol, a URL should not contain '//' 
    return -1 if url.split('://')[1].count('//') > 0 else 1

def having_sub_domain(url):
    parts = urlparse(url).netloc.split('.')
    if len(parts) > 3:
        return 0 if len(parts) == 4 else -1  # Assuming 'www' as a common subdomain
    return 1

def ssl_final_state(url):
    try:
        response = requests.head(clean_url(url), timeout=5, verify=True)
        if response.ok and urlparse(url).scheme == 'https':
            return 1
    except requests.exceptions.SSLError:
        return -1
    except:
        return 0
    return -1  # Default case if not HTTPS or connection fails

def domain_registration_length(url):
    try:
        domain_info = whois.whois(urlparse(url).netloc)
        if domain_info["domain_name"] == None: return -1
        expiration_date = domain_info.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if expiration_date:
            if (expiration_date - datetime.datetime.now()).days > 365:
                return 1
            else:
                return -1
    except:
        return 0
    return 0

def https_token(url):
    netloc = urlparse(url).netloc
    return -1 if 'https' in netloc and not netloc.startswith('https') else 1

def get_features(url):
    if not is_valid_url(url):
        return 404
    features = [
        has_ip_address(url),
        url_length(url),
        has_at_symbol(url),
        is_shortening_service(url),
        double_slash_redirecting(url),
        having_sub_domain(url),
        ssl_final_state(url),
        domain_registration_length(url),
        https_token(url)
    ]
    return features

# Example usage:
# url = "https://ozlotto.store"
# features = get_features(url)
# print(features)
