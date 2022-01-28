import requests
import json


class ConnectionScript:
    """"""
    token = 'dghfdghdgh'
    base_url = 'http://127.0.0.1:8000'
    header = {
        "Authorization": f'token {token}',
    }

    def execute(self):
        pass

    @classmethod
    def get_response(self):
        task_queue = []
        url = self.base_url + '/api/v1/task/'
        response = requests.get(url, headers=self.header)
        while response.status_code == 200 and len(response.json()) != 0:  # проверка наличия задач

            """Извлекаем по одной задаче"""
            data = response.json()
            task_queue.append(data.pop(0))
            task_id = task_queue[0]['id']
            task_url = url + f'{task_id}/'
            task = requests.get(task_url).json()

            """Передаем XML для дальнейшей обработки"""
            # requests.post('execute_url', data={'task': task['content']}, headers=self.header)

            """Статус - выполнено + response"""
            requests.patch(task_url + 'update_v/', data={
                'response': 'done',
                'is_active': False
            }, headers=self.header)

            task_queue.clear()

            response = requests.get(url, headers=self.header)

        return response.status_code


ConnectionScript.get_response()
if __name__ == '__main__':
    ConnectionScript.get_response()
