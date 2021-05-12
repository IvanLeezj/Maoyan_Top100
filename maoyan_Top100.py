import requests
from requests.exceptions import RequestException
from lxml import etree
import time

def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Cookie': '__mta=144957067.1620630420361.1620655703431.1620655910196.55; uuid_n_v=v1; uuid=503AE010B15E11EBAABD97F290011CA3A4F6133124524ED2934FC3C167DBB558; _lxsdk_cuid=1795519baecc8-0f25be27c54053-d7e1739-144000-1795519baecc8; _lxsdk=503AE010B15E11EBAABD97F290011CA3A4F6133124524ED2934FC3C167DBB558; __mta=144957067.1620630420361.1620634262925.1620634745964.13; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1620642299,1620645982,1620646103,1620655558; _csrf=d0efbb00d2701d5f15e189f139fe489c7a46d36de17ce71f3585ed1797dd0519; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1620655910; _lxsdk_s=17956994da9-1d8-ecf-d85%7C%7C45',
            'Referer' : 'https://maoyan.com/board/4'
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_page(html):
    tree = etree.HTML(html)
    dd_list = tree.xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
    for dd in dd_list:
        index = dd.xpath('./i/text()')[0]
        title = dd.xpath('./div/div/div/p[1]/a/text()')[0]
        actor = dd.xpath('./div/div/div/p[2]/text()')[0]
        release_data = dd.xpath('./div/div/div/p[3]/text()')[0]
        try:
            integer = dd.xpath('./div/div/div[2]/p/i[1]/text()')[0]
            fraction = dd.xpath('./div/div/div[2]/p/i[2]/text()')[0]
            score = integer + fraction
        except:
            score = '0.0'

        time.sleep(1)

        dic =  {
            'Index':index.strip(),
            'title':title.strip(),
            'actor':actor.strip(),
            'release_data':release_data.strip(),
            'score':score.strip()
        }
        with open('./test_new.txt', 'a', encoding='utf-8') as fp:
            fp.write(str(dic) + '\n')

def main():
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset=' + str(i*10)
        html_text = get_page(url)
        parse_page(html_text)


if __name__ == "__main__":
    main()