import MySQLdb

from photo import Photo

class PhotoList:
  def __init__(self):
    self.photos_list = []

  def load(self, offset, limit, state, cursor):
    sql = "SELECT id, fb_id, filename, caption, owner_id, state, created_at \
           FROM photos \
           WHERE state = '%s' LIMIT %d OFFSET %d" % \
           (state, limit, offset)

    try:
      cursor.execute(sql)
      data = cursor.fetchall()

      for row in data:
        photo = Photo()
        photo.load_from_tuple(row)

        self.photos_list.append(photo)

      return self.photos_list
    except Exception, e:
      raise e

  def load_before(self, timestamp, limit, state, cursor):
    sql = "SELECT id, fb_id, filename, caption, owner_id, state, \
           created_at, approved_at \
           FROM photos \
           WHERE state = %s AND approved_at < %s \
           ORDER BY approved_at DESC LIMIT %s"

    try:
      cursor.execute(sql, (state, timestamp, limit))
      data = cursor.fetchall()

      for row in data:
        photo = Photo()
        photo.load_from_tuple(row)

        self.photos_list.append(photo)

      return self.photos_list
    except Exception, e:
      raise e

  def load_after(self, timestamp, limit, state, cursor):
    sql = "SELECT id, fb_id, filename, caption, owner_id, state, \
           created_at, approved_at \
           FROM photos \
           WHERE state = %s AND approved_at > %s \
           ORDER BY approved_at ASC LIMIT %s"

    try:
      cursor.execute(sql, (state, timestamp, limit))
      data = cursor.fetchall()

      for row in data:
        photo = Photo()
        photo.load_from_tuple(row)

        self.photos_list.append(photo)

      return self.photos_list
    except Exception, e:
      raise e

  def load_by_likes(self, photo_id, db, cursor):
    # select photos where like < likes_for(photo_id)
    # union
    # select photos where like = likes_for(photo_id) and timestamp < timestamp_for(photo_id)
    curr_photo = Photo()
    curr_photo.load_from_db(photo_id, cursor)
    curr_photo_likes = curr_photo.like_count(db, cursor)
    curr_photo_approve_timestamp = curr_photo.get_dict()['approved_at']

    sql = "SELECT photos.id, photos.fb_id, photos.filename, photos.caption, \
           photos.owner_id, photos.state, photos.created_at, photos.approved_at, \
           likes_count.count \
           FROM photos \
           LEFT JOIN (SELECT photo_id, count(*) AS count FROM likes GROUP BY photo_id) AS likes_count \
           ON photos.id = likes_count.photo_id \
           WHERE likes_count.count = %s \
           AND photos.approved_at < %s \
           \
           UNION \
           \
           SELECT photos.id, photos.fb_id, photos.filename, photos.caption, \
           photos.owner_id, photos.state, photos.created_at, photos.approved_at, \
           likes_count.count \
           FROM photos \
           LEFT JOIN (SELECT photo_id, count(*) AS count FROM likes GROUP BY photo_id) AS likes_count \
           ON photos.id = likes_count.photo_id \
           WHERE likes_count.count < %s"

    try:
      cursor.execute(sql, (curr_photo_likes, curr_photo_approve_timestamp, curr_photo_likes))
      data = cursor.fetchall()

      print data

      for row in data:
        photo = Photo()
        photo.load_from_tuple(row)

        self.photos_list.append(photo)

      return self.photos_list
    except Exception, e:
      raise e
