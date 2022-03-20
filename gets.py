from typing import Optional
import requests
import dotenv
import os
from fake_useragent import UserAgent
from settings import WEBSHARE_IO_PROTOCOL


def get_proxies(
        proxy_protocol: str = WEBSHARE_IO_PROTOCOL
) -> dict:
    """
    Get context info for proxy requests: uses dotenv for https://proxy.webshare.io/
    :param proxy_protocol: 'http' or 'sock5'
    :return: dict of proxy addresses and credentials
    """
    dotenv.load_dotenv()
    proxy_address = os.getenv('PROXY_ADDRESS')
    proxy_port = os.getenv('PROXY_PORT')
    proxy_username = os.getenv('PROXY_USERNAME')
    proxy_password = os.getenv('PROXY_PASSWORD')
    assert proxy_protocol == "http" or proxy_protocol == "socks5"
    return {
        "http": f"{proxy_protocol}://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}/",
        "https": f"{proxy_protocol}://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}/"
    }


def get_headers(
        ua: str = UserAgent().chrome,
        additional_headers: Optional[dict] = None
) -> dict:
    """
    Boilerplate headers context.
    :param ua: a user-agent string
    :param additional_headers: optional dict to update the boilerplate headers with
    :return: a headers dict
    """
    headers = {
        "User-Agent": ua,
        "Accept-Language": "en-gb",
        "Accept-Encoding": "br,gzip,deflate",
        "Accept": "test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "http://www.google.com"
    }
    if additional_headers is not None:
        headers.update(additional_headers)
    return headers


def get_auth(env_user_key: str,
             env_pass_key: str) -> tuple:
    """

    :param env_user_key: Access username from .env
    :param env_pass_key: Access password from .env
    :return: Tuple of strings
    """
    return (
        os.getenv(env_user_key),
        os.getenv(env_pass_key)
    )


def get_response(
        test_url: str = "https://ipv4.webshare.io/",
        protocol: Optional[str] = WEBSHARE_IO_PROTOCOL,
        env_auth_prefix: Optional[str] = None,
        additional_headers: Optional[dict] = None
) -> requests.Response:
    """
    Send a web request with auth, headers, and proxies. Take a protocol to add proxies, a dotenv prefix to access
    auth info, and a dict to add additional headers to boilerplate headers.
    :param test_url: web address
    :param protocol: 'http' or 'sock5' or None
    :param env_auth_prefix: prefix for accessing username and password for .env file
    :param additional_headers: None or a dict with modifying headers
    :return: requests.Response object
    """
    r = requests.get(
        test_url,
        headers=get_headers(
            additional_headers=additional_headers
        ) if additional_headers is not None else get_headers(),
        proxies=None if protocol is None else get_proxies(protocol),
        auth=None if env_auth_prefix is None else get_auth(
            f"{env_auth_prefix}_USERNAME",
            f"{env_auth_prefix}_PASSWORD"
        )
    )
    r.raise_for_status()
    return r


if __name__ == "__main__":
    pass

