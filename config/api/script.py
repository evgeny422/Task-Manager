from abc import abstractmethod

import requests


# import schedule


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


class ApiConnection:
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

    def get(self, url):
        try:
            response = requests.get(url, headers=self.header)
            return response and response.status_code
        except:
            raise requests.exceptions.RequestException

    def post(self, url, data: Data):
        try:
            return requests.post(url, data=data, headers=self.header)
        except:
            raise requests.exceptions.RequestException

    def patch(self, url, data: Data):
        try:
            return requests.patch(url, data=data, headers=self.header)
        except:
            raise requests.exceptions.RequestException


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


def compare(response: dict):
    if response == 'success':
        return SuccessData().create(response)
    elif response == 'error':
        return ErrorData().create(response)

    raise Exception('Error')


class CheckTasksScript:
    task_queue = []

    def get_response(self):
        response, status = ApiConnection.get(url=ApiConnection.base_url + '/api/v1/task')

        while status == 200 and len(response.json()) != 0:
            self.task_queue.append(response.json()[0])
            task = self.task_queue.pop(0)
            task_id = task['id']
            task_info, _ = ApiConnection.get(str(ApiConnection.base_url) + f'/api/v1/task/{task_id}/')

            """Отправка задачи на выполнение"""
            response = ApiConnection.post(url='execute_url', data=task_info['content'], )
            getting_data = compare(response=response['Response'])
            processing_response = ApiConnection.patch(
                url=str(ApiConnection.base_url) + f'/api/v1/task/{task_id}/update',
                data=getting_data.get_message()
            )

            response, status = ApiConnection.get(url=ApiConnection.base_url + '/api/v1/task')

        return 'Queue is empty'


def main():
    CheckTasksScript.get_response()


if __name__ == '__main__':
    main()
