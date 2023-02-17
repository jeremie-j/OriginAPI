import requests
import random
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json
from time import time
session = requests.Session()

USER_AGENT = ' '.join([
    'Mozilla/5.0 (Zeny; EA-Origin-Auth/1.0)',
    'AppleWebKit/537.36 (KHTML, like Gecko)',
    'Chrome/71.0.3578.98 Safari/537.36'
])

BASE_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US',
    'User-Agent': USER_AGENT
}

EA_ENDPOINTS = {
    'sessionId':
        'https://signin.ea.com/p/originX/login?execution=e2062814907s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fdisplay%3DoriginXWeb%252Flogin%26response_type%3Dcode%26release_type%3Dprod%26redirect_uri%3Dhttps%253A%252F%252Fwww.origin.com%252Fviews%252Flogin.html%26locale%3Den_US%26client_id%3DORIGIN_SPA_ID',
    'authenticate':
        'https://accounts.ea.com/connect/auth?client_id=ORIGIN_JS_SDK&response_type=token&redirect_uri=nucleus%3Arest&prompt=none&release_type=prod'
}


def rnd():
    x = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return "".join([random.choice(x) for _ in range(32)])


class OriginAPI:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.access_token = {}
        self._processAuthentication(email, password)

    def _auth_get(self, url: str, headers={}):
        headers["User-Agent"] = USER_AGENT
        headers["Authorization"] = f"Bearer {self.access_token['access_token']}"
        return session.get(url, headers=headers)

    def _authed_get2(self, url, headers={}):
        headers["User-Agent"] = USER_AGENT
        headers["authtoken"] = self.access_token["access_token"]
        return requests.get(url, headers=headers)

    def _cookie_to_string(self, cookies: dict):
        plain_cookie = ""
        for name, value in cookies.items():
            plain_cookie += (name+"="+value+";")
        return plain_cookie

    def _getAuthenticationCookie(
        self,
        url: str
    ):
        session.get(url=url, headers={
            **BASE_HEADERS}, allow_redirects=False)

    def _authenticateWithCookie(self):
        if len(self.access_token.keys()) == 0:
            with open('./modules/token.json', 'r') as token:
                token_file = json.load(token)
                if token_file.get('token_expiration_date') > time():
                    self.access_token = {
                        "access_token": token_file["access_token"],
                        "token_type": token_file["token_type"],
                        'token_expiration_date': token_file['token_expiration_date']
                    }
                    return

        res = session.get(
            url=EA_ENDPOINTS["authenticate"],
            headers={
                **BASE_HEADERS, 'Cookie': self._cookie_to_string(session.cookies.get_dict())})
        res = res.json()
        self.access_token = {
            "access_token": res["access_token"],
            "token_type": res["token_type"],
            'token_expiration_date': int(time()) + int(res["expires_in"])
        }

        with open('./modules/token.json', 'w') as token:
            json.dump(self.access_token, token)

    def _preAuth(self):
        res = session.get(
            url=EA_ENDPOINTS["sessionId"],
            headers=BASE_HEADERS)
        return res.headers["selflocation"]

    def _logUser(self, credentials):
        res = session.post(
            self._preAuth(),
            headers={
                **BASE_HEADERS,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': self._cookie_to_string(session.cookies.get_dict())
            },
            data=urlencode({
                'email': credentials["email"],
                'password': credentials["password"],
                '_eventId': 'submit',
                'cid': rnd(),
                'showAgeUp': True,
                'googleCaptchaResponse': '',
                '_rememberMe': 'on'
            }),
            allow_redirects=False)
        return re.search("(?<=window\.location = \")\S+(?=\";)", res.text).group(0)

    def _processAuthentication(self, email: str, password: str):
        url = self._logUser(
            {
                "email": email,
                "password": password
            })
        self._getAuthenticationCookie(url)
        self._authenticateWithCookie()
        self._pid()

    def _pid(self):
        self.pid = self._auth_get(
            "https://gateway.ea.com/proxy/identity/pids/me").json().get("pid")

    def get_users(self, user_ids):
        res = self._authed_get2(
            f"https://api1.origin.com/atom/users?userIds={','.join(user_ids)}")
        return BeautifulSoup(res.text, features="xml")

    def search(self, origin_id, start=0):
        res = self._authed_get2(
            f"https://api1.origin.com/xsearch/users?userId={self.pid['pidId']}&searchTerm={origin_id}&start={start}")
        return res.json()

    def get_uid(self, origin_id):
        searched = self.search(origin_id)
        if searched.get("totalCount") == 0:
            return

        users = self.get_users(
            list(map(lambda user: user.get("friendUserId"), searched.get("infoList")[:5])))

        for user in users.users:
            if user.EAID.string.lower() == origin_id.lower():
                return user.userId.string

    def apex_code(self):
        res = session.get(
            f"https://accounts.ea.com/connect/auth?client_id=TITANFALL3-PC&response_type=code&redirect_uri=http://127.0.0.1/success",
            headers={**BASE_HEADERS,
                     "User-Agent": "Respawn HTTPS/1.0",
                     "access_token": self.access_token["access_token"]
                     },
            allow_redirects=False)
        self.code = re.search(
            "(?<=code=)[\S]+?(?=&|$)", res.headers["Location"]).group(0)

    def apex_data(self, user_id, hardware="PC"):
        res = requests.post(
            f"https://R5-crossplay.R5prod.stryder.respawn.com/user.php?qt=user-getinfo&hardware={hardware}&uid={user_id}",
            headers={
                "User-Agent": "Respawn HTTPS/1.0",
                "content-type": "multipart/form-data"
            })
        return json.loads("{"+res.text+"}").get('userInfo')
