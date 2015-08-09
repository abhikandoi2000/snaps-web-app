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