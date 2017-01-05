from bs4 import BeautifulSoup
import requests
import time

urls = ['https://movie.douban.com/celebrity/1054531/movies?start={}&format=text&sortby=time&'.format(str(i)) for i in range(0, 300, 25)]


# 获取某页的所有评分信息
def get_movie_ratings(web_url):
    web_data = requests.get(web_url)
    soup = BeautifulSoup(web_data.text, 'lxml')

    movie_name = soup.select('td[headers="m_name"] > a')
    date = soup.select('td[headers="mc_date"]')
    rating = soup.select('td[headers="mc_rating"]')
    role = soup.select('td[headers="mc_role"]')
    res = []

    for movie_name, date, rating, role in zip(movie_name, date, rating, role):
        '''
        data = {
            'movie': movie_name.get_text(),
            'date': date.get_text(),
            'rating': rating.get_text().strip(),
            'role': role.get_text()
        }
        '''
        rating = rating.get_text().strip()
        if rating == '':
            rating = '评分人数不足'
        elif rating == '-':
            rating = '未上映'
        data = movie_name.get_text() + '\t' + date.get_text() + '\t' + rating + '\t' + role.get_text() + '\n'
        res.append(data)

    return res


# 写入一行数据
def append_data(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()
    return 0

# 写入表头
tab_header = '电影\t年份\t评分\t角色\n'
f = open('JackieChan.txt', 'w')
f.write(tab_header)
f.close()

# 抓取并写入数据
for url in urls:
    time.sleep(2)
    lines = get_movie_ratings(url)
    print('--- getting new data from a new page ---')
    for line in lines:
        if line is not None:
            append_data('JackieChan.txt', line)
