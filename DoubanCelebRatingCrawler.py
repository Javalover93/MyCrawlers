# 输入一位影人的名字，爬取其参与电影的包含评分在内的所有信息
from bs4 import BeautifulSoup
import requests
import time


# 根据输入的关键词搜索并抓取celebrity的ID
def get_celebrity_id(celeb_name):
    celeb_id_request = 'https://movie.douban.com/celebrities/search?search_text=' + celeb_name
    web_data = requests.get(celeb_id_request)
    soup = BeautifulSoup(web_data.text, 'lxml')
    celeb_id_raw = soup.select('div.content > h3 > a')
    if len(celeb_id_raw) == 0:
        print("找不到有关信息！")
        return "celebrity not found"
    elif len(celeb_id_raw) > 1:
        print("可能存在同名的人，本程序将给出搜索结果排名第一的影人的数据。")
    celeb_id = celeb_id_raw[0].get('href').split('/')[-2]
    print(celeb_name + "的豆瓣celebrity ID是：" + celeb_id)
    return "https://movie.douban.com/celebrity/" + celeb_id + "/movies?start=0&format=text&sortby=time&"


# 根据celebrity的ID获取需要爬取的总页数
def get_total_pages():
    pass


# 获取某页的所有条目的评分信息
def get_movie_ratings():
    pass


# 写入一行数据
def append_data(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()
    return 0


if __name__ == "__main__":
    wanted_celeb_name = ""
    while len(wanted_celeb_name) == 0:
        wanted_celeb_name = input("请输入想要查询的电影人的名字：")
    url = get_celebrity_id(wanted_celeb_name)
    print(url)
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    total_pages = soup.select('head > title')[0].get_text().split('（')[-1].split('）')[0]
    print(total_pages)
    print(type(total_pages))