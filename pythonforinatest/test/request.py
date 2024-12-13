import requests


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36"
}
url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&c1=2&wd=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4'

res = requests.get(url).text
print(res)
print('====================================')
response = requests.get(url, headers=headers)
print(response.text)