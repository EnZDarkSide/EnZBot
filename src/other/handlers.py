from vbml import Pattern

# кнопки основного меню
show_schedule = 'Расписание'
open_portal = 'Портал'
show_trams = 'Трамваи'
show_trams_short = 'Т'
change_group = 'Сменить группу'

# кнопки раздела "портал"
tasks_schedule = 'Расписание заданий'
change_data = 'Сменить данные'

# меню трамваев
show_home_tram_stops = 'Домой'
show_university_tram_stops = 'В университет'
set_tram_stops = 'Задать остановки'

go_back = 'Назад'
exit_branch = 'Выйти'

regex_stop_first_letter = Pattern(r'<([147а-яА-Я])$>')
regex_stop_id = Pattern(r'<(\d+)$>')
