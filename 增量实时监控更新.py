import requests
from lxml import etree
from time import sleep
import redis
# @Time    : 2018/4/3
# @Author  : 李京阳
# @Site    :
# @File    : 块易.py
# @Software: PyCharm


class Kuai():
    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                        'Cookie':'_zendesk_shared_session=-U0xsQ1dMaGgxVXUvekRia3krZnZGbk5rZEYvbFJrb25Ia25wQ0llNkcvbzNkcUtaNlVKeUJJNlV6VDJKcGJYZ05zN2h0U0RZd1RDR3FMSWhURXdrM3BDV3pTV0hENzRCWFU2SjBKZzZvb3Voa3Z5QWhzNWQ5YXc3TlJxUWlTRHZhNERnZk5IcVoyN0tiVjlNVThZWTU3V1M0U2lIQUJwRXptWkdqUUpJT2dmbEgxdFVlTkl3cXF5NkY3aFJTRXg2RkdnRjFidTcxT3hjL2JVbVg4d21yQT09LS1SNXRRazVsKzR4clBkRGJOUWRPN1l3PT0%3D--090453c43b8d04fdd28fd9f801aec5ea798f9a27; _zendesk_session=BAh7CkkiD3Nlc3Npb25faWQGOgZFVEkiJWRlNWEzNDg0MGFmZjhlZGVmYzQ5ZGQ5YzYwZmRmODM1BjsAVEkiDGFjY291bnQGOwBGaQOLcx9JIgpyb3V0ZQY7AEZpAwKWHkkiE3dhcmRlbi5tZXNzYWdlBjsAVHsASSIOaXNfbW9iaWxlBjsAVEY%3D--99fe5d8377a4e07dc2705f0e7ae24ce0705099ad; _help_center_session=R2xTY2IvSXpWYUxzRDU3elByY2FCTTdQWWZYaDlWZFA3bGxFMVQzTjZIZTVHSkR1NzdpOEVjaTZHQmJXRTlDOXdvU0VTMWhOYmsyL0F3bHlhemZBZmRIeHFPaUw1UU9pblFtY0lGemRxa2dEOVFpODA1elcrdnBYS3AxOUZRN1V3UzJ5andoa2ZYV1lIY245Sno1VGJBPT0tLWlNeTVkakpSME54NUtrQ1EvMjNmcmc9PQ%3D%3D--591181d49db85cf6c2c7be9d7018c17d7efd1d6e'}
        self.redis = redis.Redis(host='localhost', port=6379, db=2)  # 存入redis库进行去重处理

    def get_html(self, url):
        response = requests.get(url, self.header).text  # 获取网页源码
        self.get_url(response)

    def get_url(self, url):
        html = etree.HTML(url)
        # title = html.xpath('//ul[@class="article-list"]//a/text()')
        new_url = html.xpath('//ul[@class="article-list"]//a/@href')  # 解析网页
        i = 0
        # for tit in title:
        for l in new_url:
            new_l = ('https://bibox.zendesk.com'+l)  # 拼接url连接
            print(new_l)
            self.redis.sadd('bibox', new_l)  # 将url添加进redis库
            i += 1
        print('此页共%d条数据' % i)

    def main(self):
        for i in range(1, 3+1):
            url = 'https://bibox.zendesk.com/hc/zh-cn/sections/115000986074-%E5%85%AC%E5%91%8A?page={}'.format(i)  # 拼接动态url进行翻页抓取
            self.get_html(url)

if __name__ == '__main__':
    q = Kuai()
    n = 0
    while True:
        n = n + 1
        print('已经请求%d次' % n)
        q.main()
        sleep(20)  # 20秒请求一次页面