import os
import config
import requests
from models import User

class UsersDB:
    def __init__(self, db):
        self.db = db

    def hasDataOf(self, id):
        u = User.get(id)
        if u is None:
            return False
        return True

    def add(self, id):
        r = requests.get('https://graph.facebook.com/v2.6/' + str(id), params={
            'fields': 'first_name,last_name,gender,profile_pic',
            'access_token': os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
        })
        data = r.json()
        name = data["first_name"] + " " + data["last_name"]
        user = User(id=id)
        user.add_details(name=name, first_name=data["first_name"], gender=data["gender"], pic_url=data["profile_pic"])
        self.db.session.add(user)
        self.db.session.commit()

    def get(self, id):
        user = User.get(id)
        return user