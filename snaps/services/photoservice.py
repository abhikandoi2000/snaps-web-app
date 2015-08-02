import time

from ..models.photo import Photo
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

        return {"action_performed": "unliked", "action_status": True}
      else:
        photo.like({"user_id": user_id, "created_at": int(time.time())}, db, cursor)

        return {"action_performed": "liked", "action_status": True}
    except Exception, e:
      raise e

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


