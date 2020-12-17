from vbml import Pattern

set_tram_stops = 'Задать остановки'
show_trams = 'Трамваи'
show_trams_short = 'Т'
show_home_tram_stops = 'Домой'
show_university_tram_stops = 'В университет'
exit_branch = 'Выйти'

regex_stop_first_letter = Pattern(r"<([147А-Яа-я])$>")
regex_stop_id = Pattern(r"<(\d{4,6})$>")
