import json
import pandas as pd
import configparser
import logging
import logging.config

#loggingの設定
logging.config.fileConfig('./asset/logging.ini')
logger = logging.getLogger('root')

class ProcessingGearData:
    def __init__(self) -> None:
        self.gear_id = pd.read_csv('./asset/gear_id.csv', encoding='shift-jis')

    def get_gear_info(self, gear_dict:dict, gear_type:str)->dict:
        """gear_dictから各種基礎情報を取得する。"""
        data = {}
        data['gear_name'] = gear_dict['name']
        data['gear_type'] = gear_dict['__typename']
        data['gear_id'] = gear_dict[gear_type]
        data['rarity'] = gear_dict['rarity']
        data['brand_id'] = gear_dict['brand']['id']
        data['brand_name'] = gear_dict['brand']['name']
        data['primaryGearPowerid'] = gear_dict['primaryGearPower']['gearPowerId']
        data['primaryGearPower_name'] = gear_dict['primaryGearPower']['name']
        data['additionalGearPowers'] = gear_dict['additionalGearPowers']
        data['exp'] = gear_dict['stats']['exp']
        return data

    def get_additional_gear_powers(self, gear_dict, slot)->dict:
        """gear_dictからslotを指定してサブギアを取得する。"""
        data = {}
        data['gear_name'] = gear_dict['name']
        data['gear_slot'] = slot
        data['additional_gear_power_id'] = gear_dict['additionalGearPowers'][slot]['gearPowerId']
        data['additional_gear_power'] = gear_dict['additionalGearPowers'][slot]['name']
        return data

    def get_vs_log_id(self, latest_vs_log:json)->list:
        """最新50戦のjsonから、対戦idを取得する。"""
        data = []
        for i in latest_vs_log['data']['latestBattleHistories']['historyGroups']['nodes'][0]['historyDetails']['nodes']:
            data.append(i['id'])
        return data

    def save_latest_vs_log_id(self, file_name:str, latest_vs_log:json)->None:
        """最新の対戦idをiniファイルに保存する。"""
        config = configparser.ConfigParser()
        config.read(file_name)
        vs_log_id = self.get_vs_log_id(latest_vs_log)
        try:
            config.add_section('SETTINGS')
        except configparser.DuplicateSectionError:
            pass
        config.set('SETTINGS', 'last_vs_log_id', vs_log_id[0])
        with open(file_name, 'w') as config_file:
            config.write(config_file)

    def read_last_vs_log_id(self, file_name:str)->str:
        '''iniファイルから前回の最新対戦idを取得し返す。'''
        config = configparser.ConfigParser()
        config.read(file_name)
        try:
            id = config.get('SETTINGS', 'last_vs_log_id')
            return id
        except (configparser.NoOptionError, configparser.NoSectionError):
            print('最新対戦idが保存されていません。')
            return ''    

    def get_aquired_vs_log_id_list(self, latest_vs_log:json, latest_vs_log_id:str)->list:
        """前回取得時の最新の対戦idから、詳細を取得すべき対戦idを取得し、リストとして返す。"""
        vs_log_id_list = self.get_vs_log_id(latest_vs_log)
        if latest_vs_log_id in vs_log_id_list:
            return vs_log_id_list[:vs_log_id_list.index(latest_vs_log_id)]
        print('前回取得時より50戦以上記録があります。正常にログを取得できない可能性があります。')
        return vs_log_id_list

    def add_gear_power_to_data(self, data:list, record_origin:dict, vs_detail_player:dict, gear_type:str)->list:
        """対戦ログ詳細から、サブギアを取得し、listにまとめる。"""
        record = record_origin.copy()
        record['name'] = vs_detail_player[gear_type]['name']
        record['type'] = gear_type
        for i, record_1 in enumerate(vs_detail_player[gear_type]['additionalGearPowers']):
            record['slot'] = i
            record['gear_power_name'] = record_1['name']
            data.append(record.copy())
        return data    

    def get_additional_gear_power_df(self, all_gear_dict:dict) ->pd.DataFrame:
        """イカリング3から取得しdict型にしたall_gearから、サブギアを取得しdfとして返す。"""
        data_list = []
        for record in all_gear_dict['data']['headGears']['nodes']:
            for i in range(len(record['additionalGearPowers'])):
                data_list.append(self.get_additional_gear_powers(record, i))
        for record in all_gear_dict['data']['clothingGears']['nodes']:
            for i in range(len(record['additionalGearPowers'])):
                data_list.append(self.get_additional_gear_powers(record, i))
        for record in all_gear_dict['data']['shoesGears']['nodes']:
            for i in range(len(record['additionalGearPowers'])):
                data_list.append(self.get_additional_gear_powers(record, i))
        return pd.DataFrame(data_list)#全ギアのサブギアパワーのdf

    def get_all_gear_info(self, all_gear_dict)->pd.DataFrame:
        """イカリング3から取得しdict型にしたall_gearから、ギア情報を取得しdfとして返す。"""
        data_list = []
        for record in all_gear_dict['data']['headGears']['nodes']:
            data_list.append(self.get_gear_info(record, 'headGearId'))
        for record in all_gear_dict['data']['clothingGears']['nodes']:
            data_list.append(self.get_gear_info(record, 'clothingGearId'))
        for record in all_gear_dict['data']['shoesGears']['nodes']:
            data_list.append(self.get_gear_info(record, 'shoesGearId'))
        return pd.DataFrame(data_list)#全ギアの各種情報のdf

    def get_all_additional_gear_power_from_vs_log(self, vs_log:list)->pd.DataFrame:
        """対戦ログ詳細を格納したlistから、サブギアパワー一覧を取得しdfとして返す。"""
        data = []
        for record in vs_log:
            record_origin = {}
            vs_detail = record['data']['vsHistoryDetail']
            record_origin['playedTime'] = vs_detail['playedTime']
            record_origin['id'] = vs_detail['id']
            data = self.add_gear_power_to_data(data, record_origin, vs_detail['player'], 'headGear')
            data = self.add_gear_power_to_data(data, record_origin, vs_detail['player'], 'clothingGear')
            data = self.add_gear_power_to_data(data, record_origin, vs_detail['player'], 'shoesGear')
        return pd.DataFrame(data)#対戦記録から取得できるギアパワー一覧のdf

    def get_vs_info_from_vs_log(self, vs_log:list)->pd.DataFrame:
        """対戦ログ詳細からを格納したリストから、対戦の勝敗などの結果を取得しdfで返す。ギアが取得する経験値の計算に用いる"""
        data = []
        for record in vs_log:
            record_origin = {}
            vs_detail = record['data']['vsHistoryDetail']
            if vs_detail['judgement'] == 'DRAW':
                continue
            record_origin['playedTime'] = vs_detail['playedTime']
            record_origin['id'] = vs_detail['id']
            record_origin['vs_mode'] = vs_detail['vsMode']['mode']
            record_origin['judgement'] = vs_detail['judgement']
            record_origin['paint'] = vs_detail['player']['paint']
            record_origin['knockout'] = vs_detail['knockout']
            record_origin['duration'] = vs_detail['duration']
            record_origin['vs_score'] = vs_detail['myTeam']['result']['score']
            data.append(record_origin)
        return pd.DataFrame(data)#対戦記録から取得できる対戦結果詳細のdf

    def calc_exp_for_bankara(self, judgement, knockout, duration, vs_score)->int:
        """バンカラマッチの対戦記録から基本取得経験値を計算する。"""
        if knockout == 'WIN':
            return 2500
        exp = 0
        if judgement == 'WIN':
            exp += 1500
        exp += (duration//60)*100
        exp += vs_score*5
        return (int(exp))

    def cacl_exp_for_nawabari(self, judgment, paint)->int:
        """ナワバリバトルの対戦記録から、基本取得計算値を計算する。"""
        exp = 300#タイムボーナス
        if judgment == 'WIN':
            exp += 600
        if paint >= 500:
            exp += 500
        elif paint < 100:
            exp += 100
        else:
            exp += (paint//100)*100
        return exp

    def add_base_exp_to_vs_info_df(self, vs_info:pd.DataFrame)->pd.DataFrame:
        """対戦記録のdfに基礎経験値を追加する"""
        vs_info['exp'] = vs_info.apply(
            lambda x: 
                self.calc_exp_for_bankara(x['judgement'], x['knockout'], x['duration'],x['vs_score']) 
                if x['vs_mode'] == 'BANKARA' 
                else self.cacl_exp_for_nawabari(x['judgement'], x['paint']),
            axis=1
            )

    def get_cleaning_gear_list(self, additional_gear_power_from_vs_log:pd.DataFrame)->list:
        """クリーニングされたギアの一覧を取得し、リストとして返す。"""
        return additional_gear_power_from_vs_log[
            (additional_gear_power_from_vs_log['slot']==0) 
                & 
            (additional_gear_power_from_vs_log['gear_power_name'] == 'はてな')
        ]['name'].unique()#dfのうち、1スロット目がはてなであるギアの名称リスト

    def add_new_flag(self, additonal_gear_powers_df:pd.DataFrame, 
        cleaning_gear_list:list, 
        old_additional_gear_powers_df:pd.DataFrame = pd.DataFrame(columns=['gear_name', 'gear_slot', 'additional_gear_power_id', 'additional_gear_power'])
        )->pd.DataFrame:
        """最新所持ギアのサブギアdfにis_newフラグを付与する。is_newは新しく取得か、クリーニングしたことを示す。"""
        additonal_gear_powers_df['is_new'] = False
        had_gear = old_additional_gear_powers_df['gear_name'].unique()
        additonal_gear_powers_df.loc[~additonal_gear_powers_df['gear_name'].isin(had_gear), 'is_new'] = True
        additonal_gear_powers_df.loc[additonal_gear_powers_df['gear_name'].isin(cleaning_gear_list), 'is_new'] = True
        return additonal_gear_powers_df#サブギアパワー一覧にis_newフラグを追加したdf

    def get_max_slot_of_additional_gear_power(self, old_additional_gear_powers_df:pd.DataFrame)->pd.DataFrame:
        """過去の所持ギアのサブギアdfのうちどこまでスロットが埋まっているかを取得しdfを返す。"""
        return old_additional_gear_powers_df[
            old_additional_gear_powers_df['additional_gear_power'] != 'はてな'
        ].groupby('gear_name').max('gear_slot').reset_index()[['gear_name', 'gear_slot']]

    def get_not_cleaning_additional_gear_power(self, additonal_gear_powers_df:pd.DataFrame, max_slot_of_additional_gear_power_df:pd.DataFrame)->pd.DataFrame:
        """クリーニングせずに過去のサブギアdfから更新されているサブギアパワー一覧のdfを返す。"""
        old_additonal_gear_powers_df = additonal_gear_powers_df[
            (additonal_gear_powers_df['is_new'] == False) 
                & 
            (additonal_gear_powers_df['additional_gear_power'] != 'はてな')
        ]
        additional_gear_powers_got_by_vs_df = pd.merge(old_additonal_gear_powers_df, max_slot_of_additional_gear_power_df, on='gear_name', how='left')
        additional_gear_powers_got_by_vs_df['gear_slot_y'].fillna(-1)
        additional_gear_log = additional_gear_powers_got_by_vs_df[additional_gear_powers_got_by_vs_df['gear_slot_x']-additional_gear_powers_got_by_vs_df['gear_slot_y'] > 0].copy()
        additional_gear_log['gear_slot'] = additional_gear_log['gear_slot_x'] - additional_gear_log['gear_slot_y'] -1
        return additional_gear_log[['gear_name', 'gear_slot', 'additional_gear_power_id', 'additional_gear_power', 'is_new']]
        
    def get_all_additional_gear_power(self, 
            additional_gear_powers_df:pd.DataFrame, 
            not_cleaning_additional_gear_powers_df:pd.DataFrame
        )->pd.DataFrame:
        """追加されたギアパワー一覧を取得しdfを返す。"""
        additional_gear_powers_df = additional_gear_powers_df[
            (additional_gear_powers_df['is_new'] == True) 
                & 
            (additional_gear_powers_df['additional_gear_power'] != 'はてな')
        ].copy()
        return pd.concat([additional_gear_powers_df, not_cleaning_additional_gear_powers_df])

    def get_additional_gear_log(self, 
            all_additional_gear_power:pd.DataFrame, 
            old_all_additional_gear_power:pd.DataFrame=pd.DataFrame(columns = ['gear_name', 'gear_slot', 'additional_gear_power'])
        )->pd.DataFrame:
        """ギアログをcsvファイルとして保存する。"""
        all_additional_gear_power = all_additional_gear_power[['gear_name', 'gear_slot', 'additional_gear_power']].copy()
        max_gear_log = old_all_additional_gear_power.groupby('gear_name').max('gear_slot')
        if not ('gear_slot' in max_gear_log.columns):
            max_gear_log['gear_slot'] = 0
        work = pd.merge(all_additional_gear_power, max_gear_log, on='gear_name', how='left')
        work['gear_slot_y'].fillna(-1, inplace=True)
        work['gear_slot'] = work['gear_slot_x'] + work['gear_slot_y'] + 1
        work = work[['gear_name', 'gear_slot', 'additional_gear_power']].copy()
        
        return pd.concat([old_all_additional_gear_power, work])

    def make_additional_gear_log(self, response_all_gear, response_vs_detail_list, **dfs):
        """取得したresponseを用いてギアログを作成する。"""
        additional_gear_power_df = self.get_additional_gear_power_df(response_all_gear)
        all_gear_power_from_vs_log = self.get_all_additional_gear_power_from_vs_log(response_vs_detail_list)
        cleaning_list = self.get_cleaning_gear_list(all_gear_power_from_vs_log)
        if 'old_additional_gear_powers_df' in dfs.keys():
            old_additional_gear_powers_df = dfs['old_additional_gear_powers_df']
            additional_gear_power_df.to_csv('./data/last_additional_gear_power.csv', encoding='shift-jis')
            logger.info('last_additional_gear_powerを更新しました。')
            additional_gear_power_df = self.add_new_flag(additional_gear_power_df, cleaning_list, old_additional_gear_powers_df)
            max_slot_of_additional_gear_power = self.get_max_slot_of_additional_gear_power(old_additional_gear_powers_df)
        else:
            logger.info('過去のギアパワー一覧はありません。')
            additional_gear_power_df.to_csv('./data/last_additional_gear_power.csv', encoding='shift-jis')
            logger.info('last_additional_gear_powerを更新しました。')
            additional_gear_power_df = self.add_new_flag(additional_gear_power_df, cleaning_list)
            max_slot_of_additional_gear_power = pd.DataFrame(columns=['gear_name', 'gear_slot'])
        not_cleaning_additional_gear_power = self.get_not_cleaning_additional_gear_power(additional_gear_power_df, max_slot_of_additional_gear_power)
        all_additional_gear_power = self.get_all_additional_gear_power(additional_gear_power_df, not_cleaning_additional_gear_power)
        if 'old_additional_gear_power_log' in dfs.keys():
            old_additional_gear_power_log = dfs['old_additional_gear_power_log']
            raw_gear_log = self.get_additional_gear_log(all_additional_gear_power, old_additional_gear_power_log)
            raw_gear_log.to_csv('./data/raw_gear_power_log.csv', encoding='shift-jis')
            logger.info('raw_gear_power_logを更新しました。')
            raw_gear_log.pivot(index='gear_name', columns='gear_slot', values = 'additional_gear_power').to_csv('./data/gear_power_log.csv', encoding='shift-jis')
            logger.info('gear_power_logを更新しました。')
        else:
            logger.info('過去のギアパワー取得ログはありません。')
            raw_gear_log = self.get_additional_gear_log(all_additional_gear_power)
            raw_gear_log.to_csv('./data/raw_gear_power_log.csv', encoding='shift-jis')
            logger.info('raw_gear_power_logを作成しました。')
            raw_gear_log.pivot(index='gear_name', columns='gear_slot', values = 'additional_gear_power').to_csv('./data/gear_power_log.csv', encoding='shift-jis')
            logger.info('gear_power_logを作成しました。')