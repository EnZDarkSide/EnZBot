import re
import aiohttp
from lxml import html
from bs4 import BeautifulSoup

from src.portal.models import Subject, SubjTask
from src.schedule.filters import filters


async def try_login(login: str, pwd: str):
    login_url = "https://portal.usue.ru/portal/xlogin"
    values = {'eid': login, 'pw': pwd}

    session = aiohttp.ClientSession()
    base_response = await session.post(login_url, data=values)

    if 'Необходимо войти в систему' in await base_response.text():
        return False

    return base_response, session


class PortalManager:
    def __init__(self):
        self.base_response, self.session = None, None
        self.subjects = []

    async def create(self, login, pwd):
        self.base_response, self.session = await try_login(login, pwd)
        return self

    async def get_subjects(self):

        if len(self.subjects) > 0:
            return self.subjects

        iframe_str = await self.extract_iframe_html(self.base_response, "Просмотр и изменения настроек пользователя")

        iframe_html = html.fromstring(iframe_str)

        sites_raw = iframe_html.xpath('//*[@id="sites-active"]/select[2]/option')
        result = [{'href': f"https://portal.usue.ru/portal/site/{elem.attrib['value']}", 'text': elem.text.strip()}
                  for elem in sites_raw]

        for elem in sites_raw:
            subj = Subject(name=elem.text.strip(),
                           url=f"https://portal.usue.ru/portal/site/{elem.attrib['value']}")

            subj.tasks = await self.get_tasks(subj.url)
            self.subjects.append(subj)

        await self.session.close()

        return self.subjects

    async def get_tasks(self, url, filter_name=None) -> []:

        response = await self.move_to(url)

        iframe = await self.extract_iframe_html(response, "Выдача, сбор и проверка заданий в режиме онлайн.")
        iframe_parsed = BeautifulSoup(iframe, features="lxml")

        result = []

        rows = iframe_parsed.find_all('tr')

        if filter_name is str:
            rows = [row for row in rows if filters[filter_name](row)]

        for row in rows[1:]:
            td_arr = row.find_all('td')
            task = {}
            for td in td_arr:
                if 'headers' in td.attrs:
                    task[td.attrs['headers'][0]] = td.text.strip()

            subj_task = SubjTask(name=task['title'],
                                 status=task["status"],
                                 openDate=task["openDate"],
                                 dueDate=task["dueDate"])

            result.append(subj_task)

        return result

    async def post_section_request(self, from_response, to_title):
        """Отправление запроса на получение раздела сайта(предмета) на портале"""

        r = re.compile(f'href.+" title="{to_title}"')

        resp_text = await from_response.text()
        raw_section_link = re.findall(r, resp_text)[0]

        section_link = re.findall(r'(?<=href=")(.*)(?=\" title)', raw_section_link)[0]

        response = await self.session.post(section_link)
        return response

    async def extract_iframe_html(self, from_response, to_title):
        """Получение внутреннего фрейма раздела на портале"""
        # Посылаем запрос на получение раздела
        response = await self.post_section_request(from_response, to_title)

        # Получаем внутренний фрейм
        tree = html.fromstring(await response.text())
        main_frame_link = tree.xpath('//*[@class="portletMainIframe"]/@src')[0]

        response = await self.session.get(main_frame_link)
        return await response.text()

    async def move_to(self, url):
        return await self.session.post(url)
