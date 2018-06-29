# 需求：查询地区天气
# 分析：第一步，抓取上面所有的天气信息

from html.parser import HTMLParser
from urllib import request
import pickle
import json


# 解析中国天气网HTML
class WeatherHtmlParser(HTMLParser):
    def __init__(self):
        self.flag = False
        self.weather_data = None
        super(WeatherHtmlParser, self).__init__()

    def handle_starttag(self, tag, attr):
        if tag == "script":
            self.flag = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.flag = False

    def handle_data(self, data):
        if self.flag:
            if "var hour3data=" in data:
                data = data.strip("\n")
                data = data.strip("var hour3data=")
                self.weather_data = json.loads(data)


# 全国城市天气预报代码
class CityCodeHtmlParser(HTMLParser):
    def __init__(self):
        self.flag = False
        self.city_dict = {}
        super(CityCodeHtmlParser, self).__init__()

    def handle_starttag(self, tag, attr):
        if tag == "p" or tag == "br":
            self.flag = True

    def handle_endtag(self, tag):
        if tag == "p" or tag == "br":
            self.flag = False

    def handle_data(self, data):
        if self.flag:
            if "=" in data:
                data = data.split("=")
                self.city_dict[data[1]] = data[0]




# 抓取天气信息
def getAllWeather(city='天津'):
    city = queryCityCode(city)
    if city == None:
        return None
    url_address = "http://www.weather.com.cn/weather1d/%s.shtml" % city
    req = request.Request(url_address)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
    with request.urlopen(req) as html:
        data = html.read().decode("utf-8")
        # print(data)
        html_parser = WeatherHtmlParser()
        html_parser.feed(data)
        html_parser.close()
        # print('装饰器函数内',html_parser.weather_data)
        s = []
        for x in html_parser.weather_data['7d']:
            s.append(x)
        return s


# 查询城市的编码
def queryCityCode(city_name):
    # 从网上抓取信息，本来我是想放在文件里的，博客园传不了，我稍微改造了下
    # 目前代码很丑，先做个记录吧，现在毕竟没工作，先把总体的知识过一遍再说
    def getAllCityInfo():
        url_address = "http://doc.orz520.com/a/doc/2014/0322/2100581.html"
        req = request.Request(url_address)
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
        with request.urlopen(req) as html:
            data = html.read().decode("utf-8")
            html_parser = CityCodeHtmlParser()
            html_parser.feed(data)
            html_parser.close()
            return html_parser.city_dict
    city_dict = getAllCityInfo()
    if city_name not in city_dict:
        return None
    return city_dict[city_name]

if __name__ == '__main__':
    getAllWeather()
    aa = input()