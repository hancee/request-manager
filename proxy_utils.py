# From: https://github.com/sergioparamo/blog-crawler/blob/master/src/api/utils/connection_utils.py

from bs4 import BeautifulSoup
import requests
from random import choice


def simple_get(url):
    """Perform a GET request"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        return response


def fetch_proxies_free_proxy_list():
    """Fetch proxies from free-proxy-list.net."""
    url = "https://free-proxy-list.net/"
    response = simple_get(url)
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        td_elements = soup.select(".fpl-list .table tbody tr td")
        proxies = []
        for j in range(0, len(td_elements), 8):
            ip = td_elements[j].text.strip()
            port = td_elements[j + 1].text.strip()
            anonymity = td_elements[
                j + 4
            ].text.strip()  # The 'Anonymity' column is usually at index 4

            # Only add elite proxies
            if "elite proxy" in anonymity.lower():
                proxies.append(f"{ip}:{port}")
        return list(set(proxies))  # Avoid duplicates
    return []


def build_proxies_list(proxies=None, validate=True, max_validated=10):
    if proxies is None:
        proxies = fetch_proxies_free_proxy_list()
    proxies_list = [{"http": proxy, "https": proxy} for proxy in proxies]
    if not validate:
        return proxies_list
    else:
        api_test_url = "https://httpbin.org/ip"
        working_proxies = []
        while len(working_proxies) < max_validated:
            for proxy in proxies_list:
                if len(working_proxies) >= max_validated:
                    break  # Exit the loop if we have 10 working proxies
                try:
                    response = requests.get(
                        api_test_url,
                        proxies=proxy,
                        timeout=1,  # , timeout=choice(range(1, 2**3))
                    )
                    response.raise_for_status()
                    working_proxies.append(proxy)
                    print(f"Working: {proxy}")
                except Exception as e:
                    continue  # Skip to the next proxy
        return working_proxies
