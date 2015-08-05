import time
from os import path
import json

from ..models.photo import Photo
from ..models.photolist import PhotoList
from ..models.user import User

class UserService:
  def __init__(self):
    pass

  def create(self, name, uid, email, credentials, db, cursor):
    user = User()

    try:
      return user.create((
          name, uid, "Facebook", json.dumps(credentials), \
          email, int(time.time()), 0
        ), db, cursor)
    except Exception, e:
      raise e
