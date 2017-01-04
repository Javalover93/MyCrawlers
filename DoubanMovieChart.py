from bs4 import BeautifulSoup
import requests

# 获取豆瓣电影新片榜的标题、评分和评分人数
url = 'https://movie.douban.com/chart'


def getDbMovieChart(url, data = None):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    titles = soup.select('tr.item > td:nth-of-type(1) > a')
    rating = soup.select('span.rating_nums')
    rate_people = soup.select('tr.item > td:nth-of-type(2) > div > div > span.pl')
    print(titles)

    for titles, rating, rate_people in zip(titles, rating, rate_people):
        data = {
            'titles': titles.get('title'),
            'rating': rating.get_text(),
            'rate_people': rate_people.get_text(),
        }
        print(data)

getDbMovieChart(url, data=None)
