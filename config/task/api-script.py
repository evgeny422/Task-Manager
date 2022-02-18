from abc import abstractmethod

import requests


# import schedule


class Data:
    response: str
    is_active: bool
    package_id: int

    @abstractmethod
    def create(self, item):
        pass

    def get_message(self):
        return {
            'response': self.response,
            'is_active': self.is_active,
            'status': 1,
            'package': self.package_id,
        }


class SuccessData(Data):
    def create(self, item):
        self.response = item['response']
        self.is_active = item['is_active']
        self.package_id = item['PackageID']

        return self


class ErrorData(Data):
    def create(self, item):
        return {
            'response': item['RESPONSE'],
            'is_active': False,
            'status': 1,
            'package': item['PackageID'],
        }


class Error2Data(Data):
    def create(self, item):
        return {
            'response': item['RESPONSE'],
            'is_active': False,
            'status': 1,
            'package': item['PackageID'],
        }


class Adapter:
    def compare(self, response):
        if response == 'success':
            return SuccessData().create(response)
        elif response == 'error':
            return ErrorData().create(response)
        elif response == 'error2':
            return Error2Data().create(response)
        elif response == 'error3':
            return SuccessData().create(response)

        raise Exception('Error')


class RequestServer:
    token = '7d4cc4bbef69cfdf27bf05cdf221ebbb98d2dbcd'
    header = {
        'User-Agent': 'api-script',
        "Token-api": f'{token}',
    }

    def send(self, data: Data):
        self.requerst(task_url + 'update/', data.get_message(), 'patch')

    def requerst(self, url: str, data, request_type='post'):
        if request_type == 'post':
            requests.post(url, data, headers=self.headers)
        if request_type == 'patch':
            requests.patch(url, data, headers=self.headers)


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
            #     package = requests.post('execute_url', data={'task': task['content']}, headers=self.header)
            # except requests.exceptions.RequestException as e:
            #     raise e
            #

            adapter = Adapter().compare(package)
            RequestServer.send(adapter)

            #
            # if 'Error' in package:
            #     """Если получаем ошибку"""
            #
            #     requests.patch(task_url + 'update/', data={
            #         'response': package['Error'],
            #         'is_active': False,
            #         'status': 2,
            #     }, headers=self.header)
            #
            # elif 'PackageID' in package:
            #     """При успешном выполнении"""
            #
            #     requests.patch(task_url + 'update/', data={
            #         'response': package['RESPONSE'],
            #         'is_active': False,
            #         'status': 1,
            #         'package': package['PackageID'],
            #     }, headers=self.header)
            #
            # """Статус - выполнено + response"""
            # requests.patch(task_url + 'update/', data={
            #     'response': 'done',
            #     # 'is_active': False,
            #     'status': 1,
            #     # 'package' : package,
            # }, headers=self.header)

            task_queue.clear()

            response = requests.get(url, headers=self.header)

        return response.status_code


def main():
    schedule.every(10).minutes.do(ConnectionScript.get_response())


ConnectionScript.get_response()
if __name__ == '__main__':
    main()
