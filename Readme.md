# Matrixdata sdk
获取数据超过500条时，sdk会自动进行多次访问，并进行数据拼接。方便使用。

## 获取k线数据
```
matrixdata = matrixdata_sdk(token = "your token")
    for symbol in ['BTC/USDT.BN','ETH/USDT.BN','BCC/USDT.BN','LTC/USDT.BN','ETC/USDT.BN','XRP/USDT.BN','EOS/USDT.BN']:
        params = {'symbol':symbol,
                  'interval':'5m',
                  'start':'2018-09-29 00:00:00',
                  'end':'2018-10-01 02:00:00',
                 'limit':500}
        df_bar = matrixdata.get_bar(params)
```
### 获取逐笔数据
```
matrixdata = matrixdata_sdk(token = "your token")
    for symbol in ['BTC/USDT.BN','ETH/USDT.BN','BCC/USDT.BN','LTC/USDT.BN','ETC/USDT.BN','XRP/USDT.BN','EOS/USDT.BN']:
        params = {'symbol':symbol,
                  'start':'2018-09-29 00:00:00',
                  'end':'2018-10-01 02:00:00',
                 'limit':500}

        df_trades = matrixdata.get_trades(params)
```
