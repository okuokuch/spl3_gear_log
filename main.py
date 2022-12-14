from libs import get_token
from libs import processing
import pickle
import pandas as pd
import json
import pyperclip
import logging
import logging.config
from tkinter import messagebox
import os

#loggingの設定
logging.config.fileConfig('./asset/logging.ini')
logger = logging.getLogger('root')

def is_writable(file_path):
    try:
        with open(file_path, 'a') as f:
            pass
        return True
    except PermissionError:
        logger.warn('{}が開かれており、更新できません。閉じて再実行してください。'.format(file_path))
        return False

def update_gear_log():
    path = './data'
    files_name = os.listdir(path)
    files_file_name = [f for f in files_name if os.path.isfile(os.path.join(path, f))]
    for file_name in files_file_name:
        file_path = path + '/' + file_name
        if not(is_writable(file_path)):
            messagebox.showinfo('結果','処理が異常終了しました。更新されていません。\n詳細は更新ログはlogging.iniで確認できます。')
            return
    login = get_token.Login('./data/setting.ini')
    result = login.get_results('latestBattleHistories')
    if result == False:
        logger.info('token取得用のurlを作成します。')
        user = get_token.UserAuth()
        code, url = user.get_authorize_info()
        pyperclip.copy(url)
        logger.info('urlをクリップボードにコピーしました。webブラウザでアクセスしてください。')
        codes = input('コピーしたコードを貼り付けてください。')
        login.relogin(codes, code)
        result = login.get_results('latestBattleHistories')

    logger.info('直近50戦の対戦idを取得しました。')
    gear_info = processing.ProcessingGearData()
    id = gear_info.read_last_vs_log_id('./data/setting.ini')
    aquired_vs_log_id_list = gear_info.get_aquired_vs_log_id_list(result, id)
    all_gear = login.get_results('all_gear')
    if len(aquired_vs_log_id_list) != 0:
        vs_dict_list = login.get_aquired_vs_detail_results(aquired_vs_log_id_list)
        try:
            old_additional_gear_powers_df = pd.read_csv('./data/last_additional_gear_power.csv', encoding='shift-jis', index_col=0)
            old_additional_gear_power_log = pd.read_csv('./data/raw_gear_power_log.csv', encoding='shift-jis', index_col=0)
            gear_info.make_additional_gear_log(all_gear, vs_dict_list, old_additional_gear_powers_df = old_additional_gear_powers_df, old_additional_gear_power_log = old_additional_gear_power_log)
            gear_info.save_latest_vs_log_id('./data/setting.ini', result)
        except:
            gear_info.make_additional_gear_log(all_gear, vs_dict_list)
            gear_info.save_latest_vs_log_id('./data/setting.ini', result)
    else:
        additional_gear_power_df = gear_info.get_additional_gear_power_df(all_gear)
        additional_gear_power_df.to_csv('./data/last_additional_gear_power.csv', encoding='shift-jis')
        logger.info('新たな対戦がありませんでした。last_additional_gear_powerのみ更新します。')
    messagebox.showinfo('結果','処理が終了しました。\n更新ログはlogging.iniで確認できます。')

if __name__ == '__main__':
    update_gear_log()
