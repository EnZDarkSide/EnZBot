dorm_choice = 'В каком общежитии ты находишься?'
trams_available = 'Сейчас доступны эти трамваи'
error = 'Видимо, произошла какая-то ошибка. Попробуй сделать это позже'
done = 'Готово! Данные занесены в базу'
go_back = 'Выходим'
resp_show_menu = 'Призываем меню!'
stop_choice = 'Напиши одну из остановок'
no_trams = 'Трамваев нет'
endpoint_choice = 'Куда едешь?'
getting_home_stop_first_letter = 'Напиши первую букву остановки у твоего дома'
getting_university_stop_first_letter = 'Напиши первую букву остановки твоего университета'
getting_address = 'Укажите свой адрес'
getting_home_tram_stop = 'С какой остановки ты ездишь в универ?'
getting_university_tram_stop = 'На какой остановке выходишь?'


def send_greetings():
    return f"""Приветствую! Обращайся ко мне, если необходима информация:
                - о расписании в твоей группе
                - о расписании трамваев и метро (в разработке)
                - о твоих заданиях на портале """
