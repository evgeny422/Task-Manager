import requests

from config.task.XML_validation import xml_valid


class ConnectionScript:
    """"""
    token = '7d4cc4bbef69cfdf27bf05cdf221ebbb98d2dbcd'
    base_url = 'http://localhost:8000'
    header = {
        'User-Agent': 'api-script',
        "Token-api": f'{token}',
    }

    def execute(self):
        pass

    @classmethod
    def get_response(self):
        task_queue = []
        url = self.base_url + '/api/v1/task/'
        response = requests.get(url, headers=self.header)
        content = response.json()

        """Проверка наличия активных задач"""
        while response.status_code == 200 and len(content) != 0:
            """Извлекаем по одной задаче"""
            task_queue.append(content.pop(0))
            task_id = task_queue[0]['id']
            task_url = url + f'{task_id}/'
            task = requests.get(task_url).json()
            if not xml_valid(task['content']):
                requests.patch(task_url + 'update/', data={
                    'response': 'XML not valid',
                }, headers=self.header)
                raise Exception
            """Передаем XML для валидации"""
            # try:
            #     response_validate = requests.post('validate_url', data={'task': task['content']}, headers=self.header)
            #     if response_validate is True:
            #         try:
            #             requests.post('validate_content', data={'task': task['content']}, headers=self.header)
            #         except requests.exceptions.RequestException as e:
            #             raise e
            # except requests.exceptions.RequestException as e:
            #     raise e

            """Выполнение задачи"""
            # PackageID = requests.post('execute_url', data={'task': task['content']}, headers=self.header)

            """Статус - выполнено + response"""
            requests.patch(task_url + 'update/', data={
                'response': 'done',
                'is_active': False,
                # 'package' : PackageID,
            }, headers=self.header)

            task_queue.clear()

            response = requests.get(url, headers=self.header)

        return response.status_code


ConnectionScript.get_response()
if __name__ == '__main__':
    ConnectionScript.get_response()
