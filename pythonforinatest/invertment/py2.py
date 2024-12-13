import requests
import json
import datetime
import matplotlib.pyplot as plt

# 基金代码，示例中使用了一个虚拟的基金代码
fundCode = '007539'

# 起始和截止时间
startDate = '2010-01-01'
endDate = '2020-04-05'
pageSize = 4000

# 请求头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    'Referer': f'http://fundf10.eastmoney.com/jjjz_{fundCode}.html'
}

# 构造URL
url = f'http://api.fund.eastmoney.com/f10/lsjz?&fundCode=110020&pageIndex=1&pageSize={pageSize}&startDate={startDate}&endDate={endDate}&_=1586089722912'
response = requests.get(url, headers=header)

def get_data():
    '''
    获取数据
    :return: dict
    '''
    with open('007539.txt') as f:
        line = f.readline()
        result = json.loads(line)
        date_price = {}
        for found in result['Data']['LSJZList'][::-1]:
            date_price[found['FSRQ']] = found['DWJZ']
        return date_price


with open('007539.txt') as f:
    line = f.readline()
    result = json.loads(line)

# print(result)


# 初始化变量
total = [0] * 5   # 到期后总份额
count = [0] * 5   # 每日定投次数
money = 100  # 每次定投金额

# 遍历数据，计算每个星期几的总份额和定投次数
for j in result['Data']['LSJZList'][::-1]:
    if j['JZZZL'] == '':
        continue
    else:
        weekday = int(datetime.datetime.strptime(j['FSRQ'], '%Y-%m-%d').weekday())
        DWJZ = float(j['DWJZ'])  # 净值
        total[weekday] += money / DWJZ  # 转换金额为份额并累加
        count[weekday] += 1  # 定投次数加1

# 打印结果
for i, (t, c) in enumerate(zip(total, count)):
    print(f"星期{i+1}定投最终金额：{t*DWJZ:.2f}元，定投次数：{c}")
