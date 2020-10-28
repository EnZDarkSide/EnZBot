import re

import requests
from lxml import html


class PortalParser:

    def __init__(self, login, pwd):
        self.login_url = "https://portal.usue.ru/portal/xlogin"
        self.values = {'eid': login, 'pw': pwd}

    def get_sites(self):
        result = []

        # Заходим на сайт
        response = requests.post(self.login_url, self.values)
        cookie = response.request.headers['Cookie']

        # Получаем раздел "Мои сайты"
        raw_sites_link = re.findall(r'href.+" title="Изменение и создание сайтов"', response.text)[0]
        sites_link = re.findall(r'(?<=href=")(.*)(?=\" title)', raw_sites_link)[0]

        response = requests.post(sites_link, headers={'Cookie': cookie})

        # Получаем внутренний фрейм с таблицей сайтов
        tree = html.fromstring(response.text)
        main_frame = tree.xpath('//*[@class="portletMainIframe"]/@src')[0]

        response = requests.get(main_frame, headers={'Cookie': cookie})
        tree = html.fromstring(response.text)

        # Список сайтов (кроме My Workspace)
        sites_raw = tree.xpath('//*[@target]')[1:]

        sites = [{'href': elem.attrib['href'], 'text': elem.text.strip()} for elem in sites_raw]

        return sites
