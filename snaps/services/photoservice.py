import time

from ..models.photo import Photo

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


