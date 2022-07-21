from locust import HttpUser, task, between

from test_data import *


class PostTest(HttpUser):
    host = 'http://localhost:80'
    wait_time = between(2, 4)
    token = ""
    uid = ""
    username = ""
    testPostID = ""

    def on_start(self):
        self.create_user()
        self.testPostID = self.client.post('/post/post',
                                           headers={'Authorization', self.token},
                                           json=random_Post(self.uid, self.username)).json()["postID"]

    def create_user(self):
        user = random_User()
        self.username = user["username"]
        self.client.post('/auth/register', json=user)
        login_resp = self.client.post('/auth/login', json=user).json()
        self.uid = login_resp["uid"]
        self.token = login_resp['token']

    @task
    def post_test(self):
        self.client.post('/post/post', headers={'Authorization', self.token}, json=random_Post(self.uid, self.username))

    @task
    def get_post_test(self):
        self.client.get('/post/get/' + self.testPostID, headers={'Authorization', self.token})

    @task
    def get_api_user_liked_test(self):
        self.client.get('/post/get/{}/{}'.format(self.testPostID, self.uid), headers={'Authorization', self.token})

    @task
    def recent_post_test(self):
        self.client.post('/post/recent', headers={'Authorization', self.token})

    @task
    def like_unlike_post_test(self):
        self.client.post('/post/like',
                         headers={'Authorization', self.token},
                         json={"postID": self.testPostID, "userID": self.uid})
        self.client.post('/post/unlike',
                         headers={'Authorization', self.token},
                         json={"postID": self.testPostID, "userID": self.uid})

    @task
    def get_user_posts_test(self):
        self.client.get('/post/user-post/' + self.uid,
                        headers={'Authorization', self.token})