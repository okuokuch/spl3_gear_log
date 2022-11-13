#NSOのトークンを取得するのに利用するURL
url = {
    'session_token':'https://accounts.nintendo.com/connect/1.0.0/api/session_token',
    'token':'https://accounts.nintendo.com/connect/1.0.0/api/token',
    'request_id_and_f':'https://api.imink.app/f',
    'user_info':'https://api.accounts.nintendo.com/2.0.0/users/me',
    'registrationToken':'https://api-lp1.znc.srv.nintendo.net/v3/Account/Login',
    'gtoken':'https://api-lp1.znc.srv.nintendo.net:443/v2/Game/GetWebServiceToken',
    'bulletToken':'https://api.lp1.av5ja.srv.nintendo.net/api/bullet_tokens'
}

#各種トークンを取得するリクエストのヘッダ
headers = {
    'session_token':{
        'Host':'accounts.nintendo.com',
        'Content-Type':'application/x-www-form-urlencoded',
        'Connection':'keep-alive',
        'User-Agent':'Coral/2.3.1 (com.nintendo.znca; build:2792; iOS 15.6.1) NASDK/2.3.1'
    },
    'token':{
        'Content-Type':'application/json',
        'Accept-Language':'ja-JP;q=1.0, en-JP;q=0.9',
        'User-Agent':'Coral/2.3.1 (com.nintendo.znca; build:2792; iOS 15.6.1) NASDK/2.3.1'
    },
    'request_id_and_f':{
        'User-Agent': 'NSO-Ikaring3_get_data/0.1',
        'Content-Type': 'application/json; charset=utf-8'
    },
    'user_info':{
        'Content-Type':'application/json',
        'Accept-Language':'ja-JP;q=1.0, en-JP;q=0.9',
        'User-Agent':'Coral/2.3.1 (com.nintendo.znca; build:2792; iOS 15.6.1) NASDK/2.3.1',
        'authorization':None
    },
    'registrationToken':{
        'Content-Type':'application/json',
        'Accept-Language':'ja-JP;q=1.0, en-JP;q=0.9',
        'User-Agent':'Coral/2.3.1 (com.nintendo.znca; iOS 15.6.1)',
        'x-platform':'iOS',
        'x-productversion':'2.3.1'
    },
    'gtoken':{
        'Content-Type':'application/json',
        'Accept-Language':'ja-JP;q=1.0, en-JP;q=0.9',
        'User-Agent':'Coral/2.3.1 (com.nintendo.znca; iOS 15.6.1)',
        'x-platform':'iOS',
        'authorization':None   
    },
    'bulletToken':{
        'Content-Type':'application/json',
        'x-web-view-ver':'1.0.0-216d0219',
        'Accept-Language':'ja-JP',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    }
}

#各種トークンを取得するリクエストのcontent
content = {
    'session_token':{
        'client_id':'71b963c1b7b6d119',
        'session_token_code':None,
        'session_token_code_verifier':None        
    },
    'token':{
        'client_id' : '71b963c1b7b6d119',
        'grant_type':'urn:ietf:params:oauth:grant-type:jwt-bearer-session-token',
        'session_token':None        
    },
    'request_id_and_f':{
        'token':None,
        'hash_method':None
    },
    'user_info':None,
    'registrationToken':{
        'parameter':{
            'language':None,
            'requestId':None,
            'naCountry':None,
            'timestamp':None,
            'naBirthday':None,
            'naIdToken':None,
            'f':None
        }
    },
    'gtoken':{
        'parameter':{
            'f':None,
            'timestamp':None,
            'requestId':None,
            'registrationToken':None,
            'id':'4834290508791808'
        }
    },
    'bulletToken':None
}

#イカリング3からデータを取得するリクエストのcontent
data = {
    "homepage":{
        "variables":{},
        "extensions":{
            "persistedQuery":{"version":"1","sha256Hash":"dba47124d5ec3090c97ba17db5d2f4b3"}
        }
    },
    "all_gear":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "10db4e349f3123c56df14e3adec2ee6f",
                "version": "1"
            }
        },
        "variables": {
            "cursor": "null",
            "fetchEquipments": True,
            "first": 5
        }
    },
    "vsSchedules":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "f5131603b235edce2218e71c27ed0d35610cb78c48bb44aa88e98fb37ab08cd0",
                "version": 1
            }
        },
        "id": "f5131603b235edce2218e71c27ed0d35610cb78c48bb44aa88e98fb37ab08cd0",
        "operationName": "VsSchedules",
        "variables": {
            "first": 6
        }
    },
    "gesotown":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "a43dd44899a09013bcfd29b4b13314ff",
                "version": 1
            }
        },
        "variables": {}
    },
    "myOutfits":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "81d9a6849467d2aa6b1603ebcedbddbe",
                "version": 1
            }
        },
        "variables": {}
    },
    "my_code_case_1":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "d02ab22c9dccc440076055c8baa0fa7a",
                "version": 1
            }
        },
        "variables": {}
    },
    "my_code_case_2":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "d29cd0c2b5e6bac90dd5b817914832f8",
                "version": 1
            }
        },
        "variables": {}
    },
    "my_code_detail":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "d935d9e9ba7a5b6b5d6ece7f253304fc",
                "version": 1
            }
        },
        "variables": {
            "myOutfitId": "TXlPdXRmaXQtdS1hNTRpNDQzdG1jdTN5ejZwZ25tbTox"
        }
    },
    "playHistory":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "29957cf5d57b893934de857317cd46d8",
                "version": 1
            }
        },
        "variables": {}
    },
    "challenge":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "8a079214500148bf88a8fce1d7209b90",
                "version": 1
            }
        },
        "variables": {}
    },
    "challenge_journey":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "bc71fc0264f3f72256724b069f7a4097",
                "version": 1
            }
        },
        "variables": {
            "id": "Q2hhbGxlbmdlSm91cm5leS1qb3VybmV5XzE="
        }
    },
    "catalog":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "aead379b98c14798df81f0dd3ebe6121",
                "version": 1
            }
        },
        "variables": {}
    },
    "photoAlbum":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "7e950e4f69a5f50013bba8a8fb6a3807",
                "version": 1
            }
        },
        "variables": {}
    },
    "weaponRecords":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "a0c277c719b758a926772879d8e53ef8",
                "version": 1
            }
        },
        "variables": {}
    },
    "stageRecords":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "56c46bdbdfa4519eaf7845ce9f3cd67a",
                "version": 1
            }
        },
        "variables": {}
    },
    "festRecords":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "44c76790b68ca0f3da87f2a3452de986",
                "version": 1
            }
        },
        "variables": {}
    },
    "fest":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "2d661988c055d843b3be290f04fb0db9",
                "version": 1
            }
        },
        "variables": {
            "festId": "RmVzdC1KUDpKVUVBLTAwMDAx"
        }
    },
    "fest_rankingHolders":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "58bdd28e3cf71c3bf38bc45836ee1e96",
                "version": 1
            }
        },
        "variables": {
            "festId": "RmVzdC1KUDpKVUVBLTAwMDAx"
        }
    },
    "heroRecord":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "fbee1a882371d4e3becec345636d7d1c",
                "version": 1
            }
        },
        "variables": {}
    },
    "allSchedules":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "7d4bb0565342b7385ceb97d109e14897",
                "version": 1
            }
        },
        "variables": {}
    },
    "coopResult":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "817618ce39bcf5570f52a97d73301b30",
                "version": 1
            }
        },
        "variables": {}
    },
    "VsHistoryDetail":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "2b085984f729cd51938fc069ceef784a",
                "version": 1
            }
        },
        "variables": {
            "vsResultId": None
        }
    },
    "bankaraBattleHistories":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "d8a8662345593bbbcd63841c91d4c6f5",
                "version": 1
            }
        },
        "variables": {
            "fetchCurrentPlayer": True
        }
    },
    "regularBattleHistories":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "333d0a48071b0036449e35ece577b06f",
                "version": 1
            }
        },
        "variables": {
            "fetchCurrentPlayer": True
        }
    },
    "latestBattleHistories":{
        "extensions": {
            "persistedQuery": {
                "sha256Hash": "80585ad4e4ecb674c3d8cd278adb1d21",
                "version": 1
            }
        },
        "variables": {
            "fetchCurrentPlayer": True
        }
    }

}

#ギアパワーチケット一覧
gear_ticket = (
    'なし',
    'インク効率アップ(メイン)',
    'インク効率アップ(サブ)',
    'インク回復力アップ',
    'ヒト移動速度アップ',
    'イカダッシュ速度アップ',
    'スペシャル増加量アップ',
    'スペシャル減少量ダウン',
    'スペシャル性能アップ',
    '復活時間短縮',
    'スーパージャンプ時間短縮',
    'サブ性能アップ',
    '相手インク影響軽減',
    'サブ影響軽減',
    'アクション強化'
)