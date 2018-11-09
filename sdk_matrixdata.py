import requests
import json
import pandas as pd
from datetime import datetime,timedelta
import numpy as np
import os
pd.set_option('max_colwidth',200)
pd.set_option('max_rows',500)

def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'
    return url[0:-1]

def json2dataframe(data):
    if data['Head']['Code'] == '200':
        df = pd.DataFrame.from_records(data['Result'])
        return df
    else:
        print ('error! get data',data['Head']['Code'])

class matrixdata_sdk():
    def __init__(self,token = "SYmZIOcV",debug = False):
        self.headers = headers = {"Authorization": token, "Content-type": "application/json"}
        self.debug = debug

    def request_get(self,url):
        if self.debug:
            print (url)
        for i in range(10):
            try:
                response = requests.get(url, headers=self.headers)
                result = response.json()
                return result
            except:
                print ('get data failed try it again! ' + str(i) + ' times')
                pass

    def get_bar(self,params):
        params['end'] = str(params['end'])
        url = "https://api.matrixdata.io/matrixdata/api/v1/barchart" + parse_params_to_str(params)
        result = self.request_get(url)
        df = json2dataframe(result)
        if df.shape[0] == 0:
            print ('empty dataframe')
            return df
        last_dt = datetime.strptime(df['Time'].values[-1], "%Y-%m-%dT%H:%M:%S.%fZ")
        while (last_dt - datetime.strptime(params['end'],"%Y-%m-%d %H:%M:%S")).total_seconds() < 0:
            print ('loading data to ',last_dt,'... ...',(last_dt - datetime.strptime(params['end'],"%Y-%m-%d %H:%M:%S")).total_seconds())
            params['start'] = last_dt
            url = "https://api.matrixdata.io/matrixdata/api/v1/barchart" + parse_params_to_str(params)
            result = self.request_get(url)
            temp_df = json2dataframe(result)[1:]
            if temp_df.shape[0] == 0:
                return df
            df = pd.concat((df,temp_df))
            last_dt = datetime.strptime(df['Time'].values[-1], "%Y-%m-%dT%H:%M:%S.%fZ")
        df = df.reset_index()
        return df

    def get_trades(self,params):
        if (datetime.strptime(params['end'],"%Y-%m-%d %H:%M:%S") - datetime.strptime(params['start'],"%Y-%m-%d %H:%M:%S")).total_seconds() > 3600:
            end_time = datetime.strptime(params['end'],"%Y-%m-%d %H:%M:%S")
            df = pd.DataFrame()
            while True:
                params['end'] = datetime.strptime(params['start'],"%Y-%m-%d %H:%M:%S")
                if (params['end'] - end_time).total_seconds() == 0:
                    break
                else:
                    params['end'] = params['end'] + timedelta(seconds=3600)
                if (end_time - params['end']).total_seconds() <= 0:
                    params['end'] = end_time
                df_part = self.get_trades_less1h(params)
                df = pd.concat((df,df_part))
                params['start'] = params['end']
            return df.drop_duplicates('AggregateId')
        else:
            return self.get_trades_less1h(params)

    def get_trades_less1h(self,params):
        params['end'] = str(params['end'])
        url = "https://api.matrixdata.io/matrixdata/api/v1/historicalTrades" + parse_params_to_str(params)
        result = self.request_get(url)
        df = json2dataframe(result)
        if df.shape[0] == 0:
            print ('empty dataframe',params)
            return df
        last_dt = datetime.strptime(df['Time'].values[-1], "%Y-%m-%dT%H:%M:%S.%fZ")
        while (last_dt - datetime.strptime(params['end'],"%Y-%m-%d %H:%M:%S")).total_seconds() < 0:
            print ('loading data to ',last_dt,'... ...')
            params['start'] = last_dt
            url = "https://api.matrixdata.io/matrixdata/api/v1/historicalTrades" + parse_params_to_str(params)
            result = self.request_get(url)
            temp_df = json2dataframe(result)
            new_df = pd.concat((df,temp_df))
            new_df = new_df.drop_duplicates('AggregateId')
            if new_df.shape[0] == df.shape[0]:
                return df
            else:
                df = new_df
            last_dt = datetime.strptime(df['Time'].values[-1], "%Y-%m-%dT%H:%M:%S.%fZ")
        df = df.reset_index()
        return df

if __name__ == '__main__':
    matrixdata = matrixdata_sdk(token = "sLjZ704u",debug = True)
    for symbol in ['BTC/USDT.BN','ETH/USDT.BN','BCC/USDT.BN','LTC/USDT.BN','ETC/USDT.BN','XRP/USDT.BN','EOS/USDT.BN']:
        params = {'symbol':symbol,
                  'interval':'5m',
                  'start':'2018-09-29 00:00:00',
                  'end':'2018-10-01 02:00:00',
                 'limit':500}

        df_trades = matrixdata.get_trades(params)
        print ('finish loading trades data')
        df_bar = matrixdata.get_bar(params)
        print ('finish loading bars data')
