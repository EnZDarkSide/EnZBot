import re

import requests
from lxml import html
from bs4 import BeautifulSoup


def try_login(login: str, pwd: str):
    login_url = "https://portal.usue.ru/portal/xlogin"
    values = {'eid': login, 'pw': pwd}
    base_response = requests.post(login_url, values)

    if 'Необходимо войти в систему' in base_response.text:
        return False

    cookie = base_response.request.headers['Cookie']

    return base_response, cookie


def format_tasks(tasks: []):
    result = []
    for task in tasks:
        text = f'Название: { task["title"] }\n' \
               f'Статус: { task["status"]}\n' \
               f'Выдано: { task["openDate"]}\n' \
               f'Срок сдачи: { task["dueDate"]}\n' \

        result.append(text)
    return result


class PortalManager:

    def __init__(self, login, pwd):
        self.tasks = []
        self.base_response, self.cookies = try_login(login, pwd)
        self.subjects = []

    def get_sites(self):
        iframe_str = self.extract_iframe_html(self.base_response, "Изменение и создание сайтов")

        iframe_html = html.fromstring(iframe_str)

        sites_raw = iframe_html.xpath('//*[@target]')[1:]
        result = [{'href': elem.attrib['href'], 'text': elem.text.strip()} for elem in sites_raw]

        self.subjects = result

        return result

    def get_tasks(self, url) -> []:
        response = self.move_to(url)

        iframe = self.extract_iframe_html(response, "Выдача, сбор и проверка заданий в режиме онлайн.")
        iframe_parsed = BeautifulSoup(iframe, features="lxml")

        result = []

        rows = iframe_parsed.find_all('tr')

        for row in rows[1:]:
            td_arr = row.find_all('td')
            task = {}
            for td in td_arr:
                if 'headers' in td.attrs:
                    task[td.attrs['headers'][0]] = td.text.strip()

            result.append(task)

        self.tasks = result

        return result

    def post_section_request(self, from_response, to_title):
        """Отправление запроса на получение раздела сайта(предмета) на портале"""

        r = re.compile(f'href.+" title="{to_title}"')
        raw_section_link = re.findall(r, from_response.text)[0]
        section_link = re.findall(r'(?<=href=")(.*)(?=\" title)', raw_section_link)[0]
        response = requests.post(section_link, headers={'Cookie': self.cookies})
        return response

    def extract_iframe_html(self, from_response, to_title):
        """Получение внутреннего фрейма раздела на портале"""
        # Посылаем запрос на получение раздела
        response = self.post_section_request(from_response, to_title)

        # Получаем внутренний фрейм
        tree = html.fromstring(response.text)
        main_frame_link = tree.xpath('//*[@class="portletMainIframe"]/@src')[0]
        response = requests.get(main_frame_link, headers={'Cookie': self.cookies})

        return response.text

    def move_to(self, url):
        response = requests.post(url, headers={'Cookie': self.cookies})
        return response
