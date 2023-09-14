# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/9/14 11:18
# File : request_params.py
import time

from VideoSpider.urlits.aes_e_d import encrypt_data, md5_encrypt, hmac_sha256
from VideoSpider.settings import APP_URL


def video_request_headers(aes_text, server_url: str = 'https://player.ddzyku.com:3653/api'):
    """下载视频，headers"""
    method = 'GET'
    timestamp= str(int(time.time()))
    # timestamp = '1694661806'
    guding = '55ca5c4d11424dcecfe16c08a943afdc'
    string_sign = encrypt_data(aes_text)
    key = md5_encrypt(server_url + method + timestamp + guding)
    x_player_signature = hmac_sha256(string_sign, key)
    headers = {
        'X-PLAYER-TIMESTAMP': timestamp,
        'X-PLAYER-SIGNATURE': x_player_signature,
        'X-PLAYER-METHOD': method,
        'X-PLAYER-PACK': string_sign
    }
    return headers


def video_request_params(usera_gent: str , request_token_url: str, url: str, app_url: str = APP_URL):
    """请求参数"""
    params = {}
    params['app_key'] = md5_encrypt(app_url)
    params['client_key'] = md5_encrypt(usera_gent)
    params['request_token'] = md5_encrypt(request_token_url)
    params['access_token'] = md5_encrypt(url.replace('http:', '').replace('https:', ''))
    return params


if __name__ == '__main__':
    aes_url_text = "6o000ovVjNdImxsuK4N7HLNBrhyljo000oimIKKVvVc2lM8kZvugM2xoo00oSppqmScYrQgaPrTv"
    server_url: str = 'https://player.ddzyku.com:3653/api'
    hea = video_request_headers(aes_url_text, server_url)
    # print(hea)

    app_url: str = 'www.555dy.com'
    url: str = f'{server_url}/get_play_url'
    request_token_url: str = 'https://zyz.sdljwomen.com'
    usera_gent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    params = video_request_params(app_url=app_url, url=url, request_token_url=request_token_url, usera_gent=usera_gent)
    # print(params)
