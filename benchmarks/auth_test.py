from locust import HttpUser, task, between

from test_data import random_User

user = random_User()


class AuthTest(HttpUser):
    host = 'http://localhost:80'
    wait_time = between(2, 4)
    token = ""

    def on_start(self):
        self.client.post('/auth/register', json=user)

    @task
    def login(self):
        response = self.client.post('/auth/login', json=user)
        self.token = response.json()['token']

    def on_stop(self):
        self.client.delete('/auth/remove', headers={'Authorization', self.token}, json=user)
