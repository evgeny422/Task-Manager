from abc import abstractmethod

import requests


class Data:
    """Данные для передачи на сервер"""

    response: str
    is_active: bool
    package_id: int

    @abstractmethod
    def create(self, item):
        pass

    @abstractmethod
    def get_message(self):
        pass


class SuccessData(Data):
    """Данные при успешном выполнении задачи"""

    def create(self, item):
        self.response = item['response']
        self.is_active = False
        self.package_id = item['PackageID']
        return self

    def get_message(self):
        return {
            'response': self.response,
            'is_active': self.is_active,
            'status': 1,
            'package': self.package_id,
        }


class ErrorData(Data):
    """Данные при получении ошибок"""

    def create(self, item):
        self.response = item['Exception']
        self.is_active = False
        return self

    def get_message(self):
        return {
            'response': self.response,
            'is_active': self.is_active,
            'status': 2,
        }


class ApiSettings:
    """Надстройки для взаимодействия с API"""

    token = '7d4cc4bbef69cfdf27bf05cdf221ebbb98d2dbcd'
    base_url = 'http://localhost:8000'
    header = {
        "User-Agent": 'api-script',
        "Token-api": f'{token}',
    }

    def get_param(self):
        return {
            'token': self.token,
            'base_url': self.base_url,
            'header': self.header,
        }


class HttpMethod:
    def get(self, url):
        try:
            response = requests.get(url, headers=ApiSettings.header)
            return response and response.status_code
        except:
            raise requests.exceptions.RequestException

    def post(self, url, data: Data):
        try:
            return requests.post(url, data=data, headers=ApiSettings.header)
        except:
            raise requests.exceptions.RequestException

    def patch(self, url, data: Data):
        try:
            return requests.patch(url, data=data, headers=ApiSettings.header)
        except:
            raise requests.exceptions.RequestException


class ApiConnection:
    queue = []

    @staticmethod
    def compare(response: dict):
        if response == 'success':
            return SuccessData().create(response)
        elif response == 'error':
            return ErrorData().create(response)

        raise Exception('Error')

    @staticmethod
    def get_base_task_list():
        return HttpMethod().get(url=ApiSettings.base_url + '/api/v1/task')

    def queue_extend(self, data):
        self.queue.append(data.json())
        return self.queue

    @staticmethod
    def execute(url=None, data=None):  # url - куда отправляются данные для обработки (на внешний сервер)
        response = HttpMethod().post(url=url, data=data)
        return response

    def check_tasks(self):
        base_response, status_code = self.get_base_task_list()
        while status_code == 200 and len(base_response.json()) != 0:
            task = self.queue.pop(0)
            task_id = task['id']
            task_detail_info = HttpMethod().get(url=f'{ApiSettings.base_url}' + f'/api/v1/task/{task_id}/')
            try:
                executed_data = self.execute(url='execute_url', data=task_detail_info['content'])
                """При успешном выполнении на стороне"""
                if executed_data:
                    getting_data = self.compare(response=executed_data['Response'])
                    HttpMethod().patch(
                        url=str(ApiSettings.base_url) + f'/api/v1/task/{task_id}/update',
                        data=getting_data.get_message()
                    )
            except:
                raise Exception

        return 'Queue is empty'
