# 输入一位影人的名字，爬取其参与电影的包含评分在内的所有信息
from bs4 import BeautifulSoup
import requests
import datetime
import time


# 根据输入的关键词搜索并抓取celebrity的ID
def get_celebrity_id(celeb_name):
    celeb_id_request = 'https://movie.douban.com/celebrities/search?search_text=' + celeb_name
    web_data = requests.get(celeb_id_request)
    soup = BeautifulSoup(web_data.text, 'lxml')
    celeb_id_raw = soup.select('div.content > h3 > a')
    if len(celeb_id_raw) == 0:
        print("找不到有关电影人！")
        return "celebrity not found"
    elif len(celeb_id_raw) > 1:
        print("可能存在同名的人，本程序将给出搜索结果排名第一的影人的数据。")
    celeb_id = celeb_id_raw[0].get('href').split('/')[-2]
    print(celeb_name + "的豆瓣celebrity ID是：" + celeb_id)
    return celeb_id


# 根据celebrity的ID获取需要爬取的总页数
def get_total_pages(celeb_url):
    if celeb_url == "celebrity not found":
        return ""
    web_data = requests.get(celeb_url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    total_pages = soup.select('head > title')[0].get_text().split('（')[-1].split('）')[0]
    if len(total_pages) > 0:
        return total_pages
    else:
        return ""


# 获取某页的所有条目的评分信息
def get_movie_ratings(web_url):
    web_data = requests.get(web_url)
    soup = BeautifulSoup(web_data.text, 'lxml')

    movie_name = soup.select('td[headers="m_name"] > a')
    movie_link = movie_name
    date = soup.select('td[headers="mc_date"]')
    rating = soup.select('td[headers="mc_rating"]')
    role = soup.select('td[headers="mc_role"]')
    res = []

    for movie_name, movie_link, date, rating, role in zip(movie_name, movie_link, date, rating, role):
        rating = rating.get_text().strip()
        if rating == '':
            rating = '评分人数不足'
        elif rating == '-':
            rating = '未上映'

        link = movie_link.get('href')
        data = movie_name.get_text() + '\t' + date.get_text() + '\t' + rating + '\t' + role.get_text() + '\t' + \
            link + '\n'
        res.append(data)

    return res


# 写入一行数据
def append_data(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()
    return 0


# 写入表头
def creat_file(cl_name, run_date):
    tab_header = '电影\t年份\t评分\t角色\t链接\n'
    file_name = cl_name + "_" + run_date + '.txt'
    with open(file_name, 'w') as f:
        f.write(tab_header)
    f.close()
    return file_name


if __name__ == "__main__":
    wanted_celeb_name = ""
    today = datetime.datetime.now().strftime('%Y%m%d')
    while len(wanted_celeb_name) == 0:
        wanted_celeb_name = input("请输入想要查询的电影人的名字：")
    wanted_celeb_id = get_celebrity_id(wanted_celeb_name)
    if wanted_celeb_id == "celebrity not found":
        print("找不到该电影人，程序已经退出。")
    else:
        wanted_celeb_url = "https://movie.douban.com/celebrity/" + wanted_celeb_id + "/movies?start=0&format=text&sortby=time&"
        pages = get_total_pages(wanted_celeb_url)
        if pages == "":
            print("找不到该电影人或无法获取电影数量。")
        elif len(pages) > 0:
            pages = int(pages)
            urls = ['https://movie.douban.com/celebrity/{}/movies?start={}&format=text&sortby=time&'.format(wanted_celeb_id, str(i)) for i in range(0, pages, 25)]
            f_name = creat_file(wanted_celeb_name, today)
            for url in urls:
                time.sleep(2)
                lines = get_movie_ratings(url)
                print('--- getting new data from a new page ---')
                for line in lines:
                    if line is not None:
                        append_data(f_name, line)
            print("数据抓取完毕。程序正常退出。")
        else:
            print("电影总数量获取失败。程序已结束。")

