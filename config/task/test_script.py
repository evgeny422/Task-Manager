import requests

url_auth = 'http://127.0.0.1:8000/api-auth/login/'
url_task = 'http://127.0.0.1:8000/api/v1/task/'
url_task_create = 'http://127.0.0.1:8000/api/v1/task/create'


def get_tasks():
    token = '51860d376dfd90a070e0b8d8f7fcdd5141bf31c7'
    header = {
        "Authorization": f"{token}",
    }
    url = 'http://127.0.0.1:8000/api/v1/task/'
    response = requests.get(url)
    if response.status_code == 200:
        print(len(response.json()) and response.json())
    return response.status_code


def get_task_id(id):
    url = f'http://127.0.0.1:8000/api/v1/task/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
    return response.status_code


def finish_task_id(id):
    url = f'http://127.0.0.1:8000/api/v1/task/{id}/finish'
    response = requests.get(url)
    return response.status_code


def create_task(url_, category):
    url = 'http://127.0.0.1:8000/api/v1/task/create'
    requests.post(url, data={
        'url': f'{url_}',
        'categoty': f'{category}',
    })
    return requests.status_codes


def main():
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
        url_, category = map(input().split())
        create_task(url_, category)


access_token = '7d4cc4bbef69cfdf27bf05cdf221ebbb98d2dbcd'
header = {
    'Content-Type': 'application/json',
    'Authorization': 'Token {}'.format(access_token)}

session = requests.Session()
test_url = 'http://127.0.0.1:8000/api/v1/task/'
response = session.get(url=test_url)
# print(response.json())
main()
