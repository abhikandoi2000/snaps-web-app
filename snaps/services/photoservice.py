import time
from os import path

from ..models.photo import Photo
from ..models.photolist import PhotoList
from ..models.user import User

class PhotoService:
  def __init__(self):
    pass

  def change_state(self, photo_id, new_state, db, cursor):
    photo = Photo()

    try:
      photo.load_from_db(photo_id, cursor)
      photo.set_state(new_state)
      photo.save(cursor, db)

      return True
    except Exception, e:
      raise e

  def toggle_like(self, photo_id, user_id, access_token, db, cursor):
    photo = Photo()
    user = User()

    user.load_from_db(user_id, cursor)

    if not user.verify_creds(access_token, cursor, db):
      return {"error": {"message": "Authencitity of the user failed"}, "action_status": False}

    # load the data for the photo
    photo.load_from_db(photo_id, cursor)

    # toggle the like on the photo
    try:
      if photo.check_like(user_id, db, cursor):
        photo.unlike(user_id, db, cursor)

        return {"action_performed": "photo.unlike", "action_status": True}
      else:
        photo.like({"user_id": user_id, "created_at": int(time.time())}, db, cursor)

        return {"action_performed": "photo.like", "action_status": True}
    except Exception, e:
      raise e

  def fetch_list(self, cursor, offset, limit = 10, state = "launched"):
    photolist = PhotoList()
    photos = photolist.load(offset, limit, state, cursor)

    photos = [photo.get_dict() for photo in photos]

    return photos

  def insert_into_db(self, data, db, cursor):
    photo = Photo()

    try:
      photo.create(
        (
          data['fb_id'],
          data['filename'],
          data['caption'],
          data['owner_id'],
          'unreviewed',
          int(time.time())
        )
        , db, cursor)

      return photo
    except Exception, e:
      raise e

  def upload(self, photo, filename, user_id, caption, access_token, db, cursor):
    user = User()
    user.load_from_db(user_id, cursor)

    if not user.verify_creds(access_token, cursor, db):
      return {"error": {"message": "Authencitity of the user failed"}, "action_status": False}

    photo.save(path.join("/home/abhi/projects/sdslabs/snaps-web-app/static/original", filename))

    try:
      self.insert_into_db(
        {
          "fb_id": None,
          "filename": filename,
          "caption": caption,
          "owner_id": user_id
        }, db, cursor)

      return {"action_performed": "photo.upload", "action_status": True}
    except Exception, e:
      raise e
