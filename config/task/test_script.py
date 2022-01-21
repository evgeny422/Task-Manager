import requests

url_auth = 'http://127.0.0.1:8000/api-auth/login/'
url_task = 'http://127.0.0.1:8000/api/v1/task/'
url_task_create = 'http://127.0.0.1:8000/api/v1/task/create'

user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/75.0.3770.142 Safari/537.36'

with requests.Session() as s:
    r = s.get(url_auth, headers={
        'User-Agent': user_agent_val
    })

    s.headers.update({'Referer': url_auth})

    s.headers.update({'User-Agent': user_agent_val})

    _xsrf = s.cookies.get('_xsrf', domain="http://127.0.0.1:8000/")

    post_request = s.post(url_auth, {

        'username': 'root',
        'password': 'root',
        '_xsrf': _xsrf,

    })

    g = s.get(url_task).json
    print(g)
