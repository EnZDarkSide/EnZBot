# -*- coding: utf-8 -*-
# Менеджер расписаний. Позволяет получать расписание для любого вуза.
from src.schedule_manager.schedules import ScheduleUSUE


class ScheduleManager:
    def __init__(self):
        # Методы у всех классов расписания одинаковы. Поэтому, чтобы легко можно было один заменить другим
        # мы помещаем их в словарь. Open-closed Principle из SOLID - нам не придется менять каждый раз кучу кода при
        # добавлении еще одного вуза
        self.schedules = {
            "УрГЭУ": ScheduleUSUE()
        }
