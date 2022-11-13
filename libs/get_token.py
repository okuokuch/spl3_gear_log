import base64
import random
import hashlib
import json
import requests
import configparser
import constant
import logging
import logging.config

#loggingの設定
logging.config.fileConfig('./asset/logging.ini')
logger = logging.getLogger('root')

class UserAuth():
    def __init__(self):
        """インスタンス作成時に、session_token_code_veriferとurlを作成する。"""
        self.reflesh_state_and_code_challenge()
        self.get_authorize_url()

    def __generate_random(self, length:int)->bytes:
        """lengthで指定されたバイト数の乱数を生成する。"""
        return base64.urlsafe_b64encode(random.randbytes(length))

    def __calculate_hashed_code(self, random_code:bytes) ->bytes:
        """SHA256でハッシュ化する関数。"""
        m = hashlib.sha256()
        m.update(random_code)
        hashed_code = m.digest()
        hashed_code = base64.urlsafe_b64encode(hashed_code)[:-1]
        return hashed_code

    def reflesh_state_and_code_challenge(self):
        """stateとsession_token_code_challengeを再作成する。"""
        self.state = self.__generate_random(32).decode()
        session_token_code_verifier_raw = self.__generate_random(33)
        self.session_token_code_verifier = session_token_code_verifier_raw.decode()
        self.session_token_code_challenge = self.__calculate_hashed_code(session_token_code_verifier_raw).decode()

    def get_authorize_url(self):
        """stateとsession_token_code_challengeを用いて、session_token_codeを得るためのURLを作成する。"""
        url = 'https://accounts.nintendo.com/connect/1.0.0/authorize?'
        html_param = {
        'client_id':'71b963c1b7b6d119',
        'redirect_uri':'npf71b963c1b7b6d119%3A%2F%2Fauth',
        'scope':'openid%20user%20user.birthday%20user.mii%20user.screenName',
        'session_token_code_challenge':self.session_token_code_challenge,
        'session_token_code_challenge_method':'S256',
        'response_type':'session_token_code',
        'state':self.state
        }
        for key, value in html_param.items():
            url = url + key  + '=' + value + '&'
        self.authorize_url = url

    def get_authorize_info(self):
        """本クラスの保持するsession_token_code_verifierと認証用URLを返すgetter"""
        return self.session_token_code_verifier, self.authorize_url
    
class Login():
    def __init__(self, file_name):
        config = configparser.ConfigParser()
        config.read(file_name)
        try:
            self.bullet_token = config.get('SETTINGS', 'bullet_token')
            self.gtoken = config.get('SETTINGS', 'gtoken')
        except (configparser.NoOptionError, configparser.NoSectionError):
            logger.warn('iniファイルが読み込めませんでした。')
            self.bullet_token = ''
            self.gtoken = ''

    def relogin(self, authorize_url:str, session_token_code_verifier:str):
        """認証用URLとsession_token_code_verifierからsession_token_codeを生成し、gtokenとbullet_tokenを取得する。"""
        self.authorize_url = authorize_url
        self.session_token_code_verifier = session_token_code_verifier
        self.__get_session_token_code()
        self.create_gtoken_and_bullet_token('./data/setting.ini')

    def save_token(self, file_name:str)->None:
        """tokenをiniファイルに保存する。"""
        config = configparser.ConfigParser()
        config.read(file_name)
        try:
            config.add_section('SETTINGS')
        except configparser.DuplicateSectionError:
            pass
        config.set('SETTINGS', 'bullet_token', self.bullet_token)
        with open(file_name, 'w') as config_file:
            config.write(config_file)
        config.set('SETTINGS', 'gtoken', self.gtoken)
        with open(file_name, 'w') as config_file:
            config.write(config_file)
        logger.info('gtokenとbullet_tokenをiniファイルに保存しました。')

    def __get_session_token_code(self):
        info = self.authorize_url.split('#')[1].split('&')
        self.session_token_code = info[1].split('=')[1]

    def create_url_header_data(self, method:str) ->tuple[str, dict, dict]:
        url = constant.url[method]
        header = constant.headers[method]
        data = constant.content[method]
        return url, header, data

    def create_gtoken_and_bullet_token(self, file_name):
        session_token = self.get_session_token(self.session_token_code, self.session_token_code_verifier)
        id_token, access_token = self.get_id_token_and_access_token(session_token)
        language, country, birthday = self.get_user_info(access_token)
        registration_token = self.get_registration_token(id_token, language, country, birthday)
        self.gtoken = self.get_gtoken(registration_token)
        self.bullet_token = self.get_bullet_token(self.gtoken)
        self.save_token(file_name)

    def get_session_token(self, session_token_code, session_token_code_verifier):
        url , header, data = self.create_url_header_data('session_token')
        data['session_token_code'] = session_token_code
        data['session_token_code_verifier'] = session_token_code_verifier
        response = requests.post(url, data = data, headers = header)
        session_token = json.loads(response.text)['session_token']
        logger.info('session_token作成成功')
        return session_token

    def get_id_token_and_access_token(self, session_token):
        url , header, data = self.create_url_header_data('token')
        data['session_token'] = session_token
        response = requests.post(url, json = data, headers = header)
        response_dict = json.loads(response.text)
        id_token = response_dict['id_token']
        access_token = response_dict['access_token']
        logger.info('id_token、access_token作成成功')
        return id_token, access_token

    def get_request_id_and_f_and_timestamp(self, token, hash_method) ->tuple[str, str, int]:
        url , header, data = self.create_url_header_data('request_id_and_f')
        data['token'] = token
        data['hash_method'] = str(hash_method)
        response = requests.post(url, data = json.dumps(data), headers = header)
        response_dict = json.loads(response.text)
        return response_dict['request_id'], response_dict['f'], int(response_dict['timestamp'])

    def get_user_info(self, access_token)->tuple[str, str, str]:
        url , header, data = self.create_url_header_data('user_info')
        bearer = 'Bearer ' + access_token
        header['authorization'] = bearer
        response = requests.get(url, headers=header)
        response_dict = json.loads(response.text)
        language, country, birthday = response_dict['language'], response_dict['country'], response_dict['birthday']
        logger.info('ユーザ情報取得成功')
        return language, country, birthday

    def get_registration_token(self, id_token, language, country, birthday) ->str:
        url , header, data = self.create_url_header_data('registrationToken')
        request_id, f, timestamp = self.get_request_id_and_f_and_timestamp(id_token, 1)
        data['parameter']['language']    = language
        data['parameter']['requestId']   = request_id
        data['parameter']['naCountry']   = country
        data['parameter']['timestamp']   = timestamp
        data['parameter']['naBirthday']  = birthday
        data['parameter']['naIdToken']   = id_token
        data['parameter']['f']           = f
        response = requests.post(url, data = json.dumps(data), headers = header)
        response_dict = json.loads(response.text)
        registration_token = response_dict['result']['webApiServerCredential']['accessToken']
        logger.info('registration_token作成成功')
        return registration_token

    def get_gtoken(self, registration_token) ->str:
        url , header, data = self.create_url_header_data('gtoken')
        request_id, f, timestamp = self.get_request_id_and_f_and_timestamp(registration_token, 2)
        bearer = 'Bearer ' + registration_token
        header['authorization'] = bearer
        data['parameter']['registrationToken']  = registration_token
        data['parameter']['requestId']           = request_id
        data['parameter']['timestamp']           = timestamp
        data['parameter']['f']                   = f
        response = requests.post(url, data = json.dumps(data), headers = header)
        gtoken = json.loads(response.text)['result']['accessToken']
        logger.info('gtoken作成成功')
        return gtoken

    def get_bullet_token(self, gtoken) ->str:
        url , header, data = self.create_url_header_data('bulletToken')
        cookie = {
        '_gtoken':gtoken
        }
        response = requests.post(url, headers = header, cookies = cookie)
        bullet_token = json.loads(response.text)['bulletToken']
        logger.info('bullet_token作成成功')
        return bullet_token

    def get_results(self, data_name:str) ->dict:
        url = 'https://api.lp1.av5ja.srv.nintendo.net/api/graphql'
        bearer = 'Bearer ' + self.bullet_token
        header = {
            'Content-Type':'application/json',
            'authorization':bearer,
            'x-web-view-ver':'1.0.0-216d0219',
            'Accept-Language':'ja-JP',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        }
        data = constant.data[data_name]
        cookie = {
            '_gtoken':self.gtoken,
            '_dnt':'0'
        }
        response = requests.post(url=url, data = json.dumps(data), headers = header, cookies = cookie)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            return response_dict
        else:
            logger.error('データを取得できませんでした。')
            return False

    def get_vs_detail_result(self, vs_id:str) ->dict:
        url = 'https://api.lp1.av5ja.srv.nintendo.net/api/graphql'
        bearer = 'Bearer ' + self.bullet_token
        header = {
            'Content-Type':'application/json',
            'authorization':bearer,
            'x-web-view-ver':'1.0.0-216d0219',
            'Accept-Language':'ja-JP',
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        }
        data = constant.data['VsHistoryDetail']
        data['variables']['vsResultId'] = vs_id
        cookie = {
            '_gtoken':self.gtoken,
            '_dnt':'0'
        }
        response = requests.post(url=url, data = json.dumps(data), headers = header, cookies = cookie)
        response_dict = json.loads(response.text)
        logger.info('対戦記録取得成功')
        return response_dict    

    def get_aquired_vs_detail_results(self, aquired_vs_log_id_list:list)->list:
        """取得すべき対戦id一覧から、対戦記録詳細のresponseを取得しdictを格納したlistを返す。"""
        data = []
        for id in aquired_vs_log_id_list:
            data.append(self.get_vs_detail_result(id))
        logger.info('{}件の対戦記録を取得しました。'.format(str(len(data))))
        return data