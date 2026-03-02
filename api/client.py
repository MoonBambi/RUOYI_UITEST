from urllib.parse import urlparse, urlencode, urljoin
from urllib.request import build_opener, HTTPCookieProcessor, Request
import http.cookiejar as cookiejar
import json


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        parsed = urlparse(base_url)
        scheme = parsed.scheme or "http"
        hostname = parsed.hostname or "localhost"
        netloc = hostname
        if parsed.port:
            netloc += f":{parsed.port}"
        self.server_root = f"{scheme}://{netloc}/"
        self.cookies = cookiejar.CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.cookies))

    def login(
        self,
        username: str = "admin",
        password: str = "admin123",
    ) -> dict:
        data = {
            "username": username,
            "password": password,
            "validateCode": "",
            "rememberMe": "false",
        }
        encoded = urlencode(data).encode("utf-8")
        req = Request(
            urljoin(self.server_root, "login"),
            data=encoded,
            method="POST",
        )
        req.add_header(
            "Content-Type",
            "application/x-www-form-urlencoded; charset=UTF-8",
        )
        with self.opener.open(req) as resp:
            body_bytes = resp.read()
        body = json.loads(body_bytes.decode("utf-8"))
        if body.get("code") != 0:
            raise RuntimeError(f"login failed: {body}")
        return body


def create_logged_in_client(
    base_url: str,
    username: str = "admin",
    password: str = "admin123",
) -> ApiClient:
    client = ApiClient(base_url)
    client.login(username, password)
    return client

