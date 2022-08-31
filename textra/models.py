import json

import requests
from requests_oauthlib import OAuth1


class ApiResultCode:
    message_dict = {
        0: '成功',
        500: 'API keyエラー',
        501: 'nameエラー',
        502: 'リクエスト上限エラー(日)',
        504: 'リクエスト上限エラー(分)',
        505: 'リクエスト上限エラー(同時リクエスト)',
        510: 'OAuth認証エラー',
        511: 'OAuthヘッダエラー',
        520: 'アクセスURLエラー',
        521: 'アクセスURLエラー',
        522: 'リクエストkeyエラー',
        523: 'リクエストnameエラー',
        524: 'リクエストパラメータエラー',
        525: 'リクエストパラメータエラー(送信データサイズ制限)',
        530: '権限エラー',
        531: '実行エラー',
        532: 'データ無し',
    }

    @classmethod
    def is_error(cls, code: int) -> bool:
        return code != 0

    @classmethod
    def get_message(cls, code: int) -> str:
        return cls.message_dict.get(code, 'unknown code')


class ApiException(Exception):
    def __init__(self, code: int) -> None:
        super().__init__(f'{code} {ApiResultCode.get_message(code)}')


class ApiClient:
    '''TexTraAPIクライアント'''
    API_URL_BASE = 'https://mt-auto-minhon-mlt.ucri.jgn-x.jp/api/mt/'

    def __init__(self, name: str, key: str, secret: str) -> None:
        self.name = name
        self.key = key
        self.secret = secret

    def post(self, path: str, text: str) -> str:
        url = f'{self.API_URL_BASE}{path}/'
        data = {
            'key': self.key,
            'name': self.name,
            'type': 'json',
            'text': text,
        }
        res = requests.post(url, data=data, auth=OAuth1(self.key, self.secret))
        resultset = json.loads(res.text)['resultset']
        if (ApiResultCode.is_error(code := resultset['code'])):
            raise ApiException(code)
        return resultset['result']['text']

    def generalNT_en_ja(self, text: str) -> str:
        '''汎用NT 【英語 - 日本語】'''
        return self.post('generalNT_en_ja', text)

    def minnaPE_en_ja(self, text: str) -> str:
        '''みん翻PE 【英語 - 日本語】'''
        return self.post('minnaPE_en_ja', text)

    def generalNT_ja_en(self, text: str) -> str:
        '''汎用NT 【日本語 - 英語】'''
        return self.post('generalNT_ja_en', text)

    def minnaPE_ja_en(self, text: str) -> str:
        '''みん翻PE 【日本語 - 英語】'''
        return self.post('minnaPE_ja_en', text)
