from locust import HttpUser, task, between

from test_data import random_User


class AuthTest(HttpUser):
    host = 'http://localhost:80'
    wait_time = between(2, 4)
    user = random_User()
    token = ""

    @task
    def register_and_login(self):
        self.client.post('/auth/register', json=self.user)
        response = self.client.post('/auth/login', json=self.user)
        self.token = response.json()['token']

    def on_stop(self):
        self.client.delete('/auth/remove', headers={'Authorization', self.token}, json=self.user)
