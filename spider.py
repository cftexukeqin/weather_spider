import requests
from bs4 import BeautifulSoup as bs
import urllib3
from pyecharts import Bar
urllib3.disable_warnings()
data_lists = []
def get_data(url):

    resp = requests.get(url,verify=False)
    resp.encoding = "utf-8"
    soup = bs(resp.text,"html5lib")
    conMidtab = soup.find("div",class_="conMidtab")
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all("tr")[2:]
        for tr in trs:
            # tds = tr.find_all("td")
            # city_td = tds[0]
            # city = list(city_td.stripped_strings)[0]
            # print(city)
            city_td = tr.find_all("td")[0]
            min_temp_td = tr.find_all("td")[-2]
            city = city_td.get_text().strip()
            min_temp = min_temp_td.get_text().strip()
            data_lists.append({'city':city,"min_temp":int(min_temp)})
    return data_lists
def main():
    urls = [
        "http://www.weather.com.cn/textFC/hb.shtml",
        "http://www.weather.com.cn/textFC/hd.shtml",
        "http://www.weather.com.cn/textFC/db.shtml",
        "http://www.weather.com.cn/textFC/hz.shtml",
        "http://www.weather.com.cn/textFC/hn.shtml",
        "http://www.weather.com.cn/textFC/xb.shtml",
        "http://www.weather.com.cn/textFC/xn.shtml",
        "http://www.weather.com.cn/textFC/gat.shtml",
    ]
    for url in urls:
        get_data(url)
    # 根据列表的结构，按照温度进行排序
    data_lists.sort(key=lambda data:data['min_temp'])

    all_data = data_lists[0:10]
    cities = list(map(lambda x:x['city'],all_data))
    temps = list(map(lambda x:x['min_temp'],all_data))

    # 生成pyecharts
    # 横轴和纵轴都需要列表
    bar = Bar('全国气温最低排行')
    bar.add("气温",cities,temps)
    bar.render('temp.html')


if __name__ == '__main__':
    main()