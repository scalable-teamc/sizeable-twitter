import random
import string

letters = string.ascii_lowercase


def random_User():
    return {
        "username": "user" + ''.join(random.choice(letters) for _ in range(4)),
        "password": ''.join(random.choice(letters) for _ in range(8))
    }


def random_Profile(uid, username):
    return {
        "uid": uid,
        "username": username,
        "image": "",
        "type": "",
        "display_name": username + ''.join(random.choice(letters) for _ in range(4)),
        "description": ''.join(random.choice(letters) for _ in range(20))
    }


def random_Post(uid, username):
    return {
        "uid": uid,
        "username": username,
        "content": ''.join(random.choice(letters) for _ in range(40)),
        "image": None
    }
