import requests

url_auth = 'http://127.0.0.1:8000/api-auth/login/'
url_task = 'http://127.0.0.1:8000/api/v1/task/'
url_task_create = 'http://127.0.0.1:8000/api/v1/task/create'


def get_tasks():
    token = '51860d376dfd90a070e0b8d8f7fcdd5141bf31c7'
    header = {
        "Authorization": f"{token}"
    }
    url = 'http://127.0.0.1:8000/api/v1/task/'
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        return len(response.json()) and response.json()
    return response.status_code


def get_task_id(id):
    url = f'http://127.0.0.1:8000/api/v1/task/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return response.status_code


def delete_task_id(id):
    url = f'http://127.0.0.1:8000/api/v1/task/{id}/delete'
    response = requests.get(url)
    return response.status_code


def create_task(url_, category, user):
    url = 'http://127.0.0.1:8000/api/v1/task/create'
    requests.post(url, data={
        'url': f'{url_}',
        'categoty': f'{category}',
        'user': f'{user}'
    })
    return requests.status_codes


def main():
    q = str(input('Действие '))
    if q == 'Список задач':
        get_tasks()
    elif q == 'Просмотреть задачу':
        _id = input('id')
        get_task_id(_id)
    elif q == 'Удалить задачу(метка не даст выводиться задаче в task-list':
        _id = input('id')
        delete_task_id(_id)
    elif q == 'Создать задачу':
        url_, category, user = map(input().split())
        create_task(url_, category, user)


# print(main())

# print(main())
# print(get_tasks())


header = {
    "Authorization": "51860d376dfd90a070e0b8d8f7fcdd5141bf31c7",
}

test_url = 'http://127.0.0.1:8000/api/v1/task/'
response = requests.get(test_url, headers=header)
print(response.json())
