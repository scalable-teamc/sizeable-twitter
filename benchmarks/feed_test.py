from locust import HttpUser, task, between

from test_data import *


class FeedTest(HttpUser):
    host = 'http://localhost:80'
    token = ""
    uid = ""
    username = ""

    def on_start(self):
        self.create_user()
        for i in range(10):
            self.client.post('/post/post', headers={'Authorization', self.token},
                             json=random_Post(self.uid, self.username))

    def create_user(self):
        user = random_User()
        self.username = user["username"]
        self.client.post('/auth/register', json=user)
        login_resp = self.client.post('/auth/login', json=user).json()
        self.uid = login_resp["uid"]
        self.token = login_resp['token']

    @task
    def get_all_feed(self):
        self.client.post('/feed/all',
                         headers={'Authorization', self.token},
                         json={"uid": self.uid, "offset": 0})
