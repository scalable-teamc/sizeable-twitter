from locust import HttpUser, task, between

from test_data import *


class ProfileTest(HttpUser):
    host = 'http://localhost:80'
    wait_time = between(2, 4)
    token = ""
    token2 = ""
    profile = dict()
    profile2 = dict()

    def on_start(self):
        self.create_user()
        self.create_2nd_user()

    def create_user(self):
        user = random_User()
        username = user["username"]
        self.client.post('/auth/register', json=user)
        login_resp = self.client.post('/auth/login', json=user).json()
        uid = login_resp["uid"]
        self.token = login_resp['token']
        profile = random_Profile(uid, username)
        self.client.post('/profile/save', headers={'Authorization', self.token}, json=profile)
        self.profile = profile

    def create_2nd_user(self):
        user = random_User()
        username = user["username"]
        reg_resp = self.client.post('/auth/register', json=user).json()
        uid2 = reg_resp["uid"]
        profile = random_Profile(uid2, username)
        self.client.post('/profile/save', headers={'Authorization', self.token}, json=profile)
        self.profile2 = profile

    @task
    def get_profile(self):
        self.client.post('/profile/getprof',
                         headers={'Authorization', self.token},
                         json={"uid": self.profile.get("uid"), "username": self.profile.get("username")})

    @task
    def get_by_username(self):
        self.client.post('/profile/getuser',
                         headers={'Authorization', self.token},
                         json={"username": self.profile.get("username")})

    @task
    def following_and_unfollow(self):
        self.client.post('/profile/follow',
                         headers={'Authorization', self.token},
                         json={"uid": self.profile.get("uid"), "following_id": self.profile2.get("uid")})
        self.client.patch("/profile/unfollow",
                          headers={'Authorization', self.token},
                          json={"uid": self.profile.get("uid"), "remove_id": self.profile2.get("uid")})

    @task
    def get_follow_info(self):
        self.client.post("/profile/getfollow",
                         headers={'Authorization', self.token},
                         json={"uid": self.profile.get("uid")})

    @task
    def get_short(self):
        self.client.get("/profile/getshort/{}".format(self.profile),
                        headers={'Authorization', self.token})

    @task
    def saved_post(self):
        self.client.post("/profile/savedPost",
                         headers={'Authorization', self.token},
                         json={"uid": self.profile.get("uid"), "post_id": random.randint(1, 20)})

    @task
    def unsaved_post(self):
        self.client.patch("/profile/unsavedPost",
                          headers={'Authorization', self.token},
                          json={"uid": self.profile.get("uid"), "post_id": random.randint(1, 20)})
