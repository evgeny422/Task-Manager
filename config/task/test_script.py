import requests

url_auth = 'http://127.0.0.1:8000/api-auth/login/'
url_task = 'http://127.0.0.1:8000/api/v1/task/'
url_task_create = 'http://127.0.0.1:8000/api/v1/task/create'
access_token = '7d4cc4bbef69cfdf27bf05cdf221ebbb98d2dbcd'


def get_tasks():
    """Get task-list"""

    token = '51860d376dfd90a070e0b8d8f7fcdd5141bf31c7'
    header = {
        "Authorization": f"{token}",
    }
    url = 'http://127.0.0.1:8000/api/v1/task/'
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
    return response.status_code


def get_task_id(id):
    """Get task/{task-id}"""

    url = f'http://127.0.0.1:8000/api/v1/task/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
    return response.status_code


def finish_task_id(id):
    """Soft-delete method"""

    url = f'http://127.0.0.1:8000/api/v1/task/{id}/finish'
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
    return response.status_code


def create_task(url_, category):
    """Create task"""

    url = f'http://127.0.0.1:8000/api/v1/create_from_get/?url={url_}&cat={category}'
    print(url)
    requests.get(url)
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
    return response.status_code


def update_task():
    """Or use HEADERS?"""

    id_ = int(input('Номер задачи: '))
    task = str(input('Что вы хотите изменить?: '))
    if task == 'cat':
        cat_ = int(input('Категория: '))
        url = f'http://127.0.0.1:8000/api/v1/task/{id_}/update/?cat={cat_}'
        requests.get(url)
        print(url)
    elif task == 'url':
        url_ = str(input('URL: '))
        requests.get(f'http://127.0.0.1:8000/api/v1/task/{id_}/update/?url={url_}')
    else:
        cat_ = int(input('Категория: '))
        url_ = str(input('URL: '))
        requests.get(f'http://127.0.0.1:8000/api/v1/task/{id_}/update/?url={url_}&cat={cat_}')


def main():
    """Pick what to do"""

    q = str(input('Действие '))
    if q == 'Список задач':
        get_tasks()
    elif q == 'Просмотреть задачу':
        _id = input('id ')
        get_task_id(_id)
    elif q == 'Завершить':
        _id = input('id ')
        finish_task_id(_id)
    elif q == 'Создать задачу':
        url_ = str(input('URL: '))
        category = int(input('Введите категорию: '))
        create_task(url_, category)
    elif q == 'Обновить':
        update_task()


main()

if __name__ == '__main__':
    main()
