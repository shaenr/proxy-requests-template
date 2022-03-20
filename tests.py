import unittest
from gets import get_response

GOOGLE = "https://www.google.com"


class TestHttpRequests(unittest.TestCase):
    def test_auth_prefix_request(self):
        r = get_response("https://bandcamp.com", env_auth_prefix="BC")
        self.assertEqual(r.status_code, 200)

    def test_default_auth_prefix(self):
        r = get_response(GOOGLE, env_auth_prefix="DEFAULT")
        self.assertEqual(r.status_code, 200)

    def test_unauthorized_request(self):
        r = get_response(GOOGLE)
        self.assertEqual(r.status_code, 200)

    def test_additional_headers(self):
        additional_headers = {"User-Agent": "DELETED", "Added": "Header123"}
        r = get_response(GOOGLE, additional_headers=additional_headers)
        user_agent = r.request.headers['User-Agent']
        added = r.request.headers['Added']
        self.assertEqual(user_agent, 'DELETED')
        self.assertEqual(added, 'Header123')

    def test_proxy_http_protocol_different_ips(self):
        http_r_ip = get_response("https://ipv4.webshare.io", protocol="http").text
        http_r_ip2 = get_response("https://ipv4.webshare.io", protocol="http").text
        self.assertNotEqual(http_r_ip, http_r_ip2)

    def test_proxy_sock5_protocol_different_ips(self):
        s5_r_ip = get_response("https://ipv4.webshare.io", protocol="socks5").text
        s5_r_ip2 = get_response("https://ipv4.webshare.io", protocol="socks5").text
        self.assertNotEqual(s5_r_ip, s5_r_ip2)


