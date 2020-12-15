import json
import random
from datetime import datetime

import requests


class ScheduleUSUE:
    @staticmethod
    def get_list_of_groups(group_pattern):
        response = requests.get(f'https://www.usue.ru/schedule/?action=group-list&term={group_pattern}')
        return json.loads(response.text)

    @staticmethod
    def get_schedule(group: str, start_date='', end_date=''):
        start_date = datetime.today().strftime('%d.%m.%Y') if start_date == '' else start_date
        end_date = datetime.today().strftime('%d.%m.%Y') if end_date == '' else end_date

        response = requests.get(f'https://www.usue.ru/schedule/?t={random.random()}&action=show'
                                f'&startDate={start_date}'
                                f'&endDate={end_date}'
                                f'&group={group}')

        print(response.url)

        return ScheduleUSUE.format(json.loads(response.text))

    @staticmethod
    def format(days):
        days_arr = []

        for i, day in enumerate(days):
            text = f'{"_" * 26 if i != 0 else ""} \n' \
                   f'📅 День недели: {day["weekDay"]}\n' \
                   f'📅 Дата: {day["date"]}\n\n' \
 \
            day['pairs'] = list(filter(lambda x: len(x['schedulePairs']) > 0, day['pairs']))

            if len(day['pairs']) == 0:
                text += 'На этот день пар нет. Отдыхайте :)'

            else:
                for pair_time in day['pairs']:

                    pairs_count = len(pair_time['schedulePairs'])

                    for (index, pair) in enumerate(pair_time['schedulePairs']):
                        pair_number = f'{index + 1}. ' if pairs_count > 1 else ''

                        text += f'{pair["subject"]}\n' \
                                f'Группа: {pair["group"]}\n' \
                                f'Преподаватель: {pair["teacher"]}\n' \
                                f'Место: {pair["aud"]}\n' \
 \
                        text += f"⌚ : {pair_time['time']} {'(ИДЕТ СЕЙЧАС)' if pair_time['isCurrentPair'] else ''}\n\n" \
 \
            days_arr.append(text)

        return days_arr
