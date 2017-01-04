from bs4 import BeautifulSoup
import requests
import time

# 小区列表页，使用安居客的数据
pages = ['http://tai.fang.anjuke.com/loupan/all/p{}/'.format(str(i)) for i in range(1, 2, 1)]


# 获取小区详情页
def get_page_urls(house_list_pages):
    page_url = []
    for page in house_list_pages:
        time.sleep(2)
        web_data = requests.get(page)
        soup = BeautifulSoup(web_data.text, 'lxml')
        page_url_raw = soup.select('a.items-name')

        for i in page_url_raw:
            page_url.append(i.get('href'))
    return page_url


# 获取并返回房价信息
def get_house_data(house_page):
    time.sleep(2)
    web_data = requests.get(house_page)
    soup = BeautifulSoup(web_data.text, 'lxml')
    xiao_qu = soup.select('#j-triggerlayer')
    di_zhi = soup.select('span.lpAddr-text')
    cheng_qu = di_zhi
    jun_jia = soup.select('em.sp-price')

    for xiao_qu, cheng_qu, di_zhi, jun_jia in zip(xiao_qu, cheng_qu, di_zhi, jun_jia):
        data = {
            'xiao_qu': xiao_qu.get_text(),
            'cheng_qu': cheng_qu.get_text()[2:4],
            'di_zhi': di_zhi.get_text()[12:],
            'jun_jia': jun_jia.get_text(),
        }
        return data['cheng_qu'] + '\t' + data['xiao_qu'] + '\t' + data['di_zhi'] + '\t' + data['jun_jia'] + '\n'


# 添加新的数据到txt
def append_data(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()

urls = get_page_urls(pages)
# 写入表头
tab_header = '城区\t小区\t地址\t均价\t'
f = open('housing.txt', 'w')
f.write(tab_header + '\n')
f.close()

# 抓取数据并保存到txt
for url in urls:
    line = get_house_data(url)
    if line is not None:
        append_data('housing.txt', line)
