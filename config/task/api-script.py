import requests
import schedule


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
        task_response = requests.get(url, headers=self.header)
        content = task_response.json()

        """Проверка наличия активных задач"""
        while task_response.status_code == 200 and len(content) != 0:
            """Извлекаем по одной задаче"""
            task_queue.append(content.pop(0))
            task_id = task_queue[0]['id']
            task_url = url + f'{task_id}/'
            task = requests.get(task_url).json()

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

            # """Выполнение задачи"""
            # try:
            #     response = requests.post('execute_url', data={'task': task['content']}, headers=self.header)
            # except requests.exceptions.RequestException as e:
            #     raise e
            #
            # if 'Error' in response:
            #     """Если получаем ошибку"""
            #
            #     requests.patch(task_url + 'update/', data={
            #         'task_response': str(response['RESPONSE']),
            #         'is_active': False,
            #         'status': 2,
            #     }, headers=self.header)
            #
            # elif 'PackageID' in response:
            #     """При успешном выполнении"""
            #
            #     requests.patch(task_url + 'update/', data={
            #         'task_response': str(response['RESPONSE']),
            #         'is_active': False,
            #         'status': 1,
            #         'package': response['PackageID'],
            #     }, headers=self.header)

            """Статус - выполнено + task_response"""
            requests.patch(task_url + 'update/', data={
                'task_response': 'w8',
                # 'is_active': False,
                'status': 1,
                # 'package' : package,
            }, headers=self.header)

            task_queue.clear()

            task_response = requests.get(url, headers=self.header)

        return task_response.status_code


def main():
    schedule.every(10).minutes.do(ConnectionScript.get_response())


ConnectionScript.get_response()
if __name__ == '__main__':
    main()
