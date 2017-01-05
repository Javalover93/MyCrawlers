from bs4 import BeautifulSoup
import requests
import time

urls = ['https://movie.douban.com/celebrity/1054531/movies?start={}&format=text&sortby=time&'.format(str(i)) for i in range(0, 300, 25)]


# 判断是不是动作片
def is_action(genre):
    for i in genre:
        if i.get_text() == '动作':
            return True
    return False


# 判断是否成龙主演的电影
def is_jackiechan_movie(movie_url):
    time.sleep(1)
    web_data = requests.get(movie_url)
    soup = BeautifulSoup(web_data.text, 'lxml')

    actors_list = soup.select('span.actor > span.attrs')
    movie_attr = soup.select('#info > span.pl')
    actors = actors_list[0].get_text().split(' / ') if len(actors_list) != 0 else []
    main_actors = actors[0:2] if len(actors) >= 2 else actors
    if len(movie_attr) > 0:
        is_movie = True if movie_attr[-1].get_text()[0:4] == 'IMDb' else False
    else:
        is_movie = False
    genre = soup.select('#info > span[property="v:genre"]')
    action = is_action(genre)
    is_jackiechan = True if '成龙' in main_actors else False
    return is_movie & is_jackiechan & action


# 获取某页的所有评分信息
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

        link = movie_link.get('href')
        is_jack = is_jackiechan_movie(link) if rating not in ['未上映','评分人数不足'] else '-'
        data = movie_name.get_text() + '\t' + date.get_text() + '\t' + rating + '\t' + role.get_text() + '\t' + \
            link + '\t' + str(is_jack) + '\n'
        res.append(data)

    return res


# 写入一行数据
def append_data(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()
    return 0

# 写入表头
tab_header = '电影\t年份\t评分\t角色\t链接\t成龙电影\n'
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
