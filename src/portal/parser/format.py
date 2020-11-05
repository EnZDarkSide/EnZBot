def format_tasks(tasks: []):
    result = []
    for task in tasks:
        text = f'Название: {task["title"]}\n' \
               f'Статус: {task["status"]}\n' \
               f'Выдано: {task["openDate"]}\n' \
               f'Срок сдачи: {task["dueDate"]}\n'
        result.append(text)
    return result
