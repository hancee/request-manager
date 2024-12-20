import requests
import numpy as np
from functools import partial
from random import choice
from src.utils.proxy_utils import build_proxies_list
from src.utils.scraper.creds import partial_headers


class RequestManager:
    def __init__(self, proxy_limit=4):
        self.timeout_choices = self._generate_timeout_choices()
        self.proxy_choices = self._generate_proxies(proxy_limit)
        self.user_agent_choices = self._generate_user_agents()

    @staticmethod
    def _generate_timeout_choices():
        """Generate a list of timeout choices with noise."""
        # Variable timeout
        right_tail_timeout_choices = np.arange(2**4, 2**6, 2)
        noise_choices = np.arange(2**4, 2**6, 1) / 100
        noisy_right_tail_timeout_choices = [
            timeout_choice + choice(noise_choices)
            for timeout_choice in right_tail_timeout_choices
        ]

        random_timeout_choices = np.arange(2**2, 2**4, 0.1)
        timeout_choices = [
            float(np.round(timeout_choice, 2)) * (2**6 / 100)
            for timeout_choice in [
                *random_timeout_choices,
                *random_timeout_choices,
                *random_timeout_choices,
                *noisy_right_tail_timeout_choices,
                *noisy_right_tail_timeout_choices,
            ]  # Introduce weights 3 random : 2 right tailed
        ]
        return timeout_choices

    @staticmethod
    def _generate_proxies(proxy_limit):
        """Build and validate a list of proxies."""
        return build_proxies_list(max_validated=proxy_limit)

    @staticmethod
    def _generate_user_agents():
        """Provide a list of user-agent strings."""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.41",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        ]

    def get_partial_request(self):
        """Generate a partial function for requests.get with randomized parameters."""
        return partial(
            requests.get,
            proxies=choice(self.proxy_choices),
            timeout=choice(self.timeout_choices),
            headers={"User-Agent": choice(self.user_agent_choices), **partial_headers},
        )
