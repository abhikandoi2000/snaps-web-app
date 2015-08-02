import MySQLdb

class Photo:
  def __init__(self):
    self.data = {
      "id": None,
      "fb_id": None,
      "filename": None,
      "caption": None,
      "owner_id": None,
      "state": None,
      "created_at": None
    }

  def load_from_db(self, photo_id, cursor):
    sql = "SELECT id, fb_id, filename, caption, owner_id, state, created_at \
           FROM photos \
           WHERE id = %d" % photo_id

    try:
      cursor.execute(sql)
      data = cursor.fetchone()

      self.load_from_tuple(data)
      print data

      return "Hello"
    except Exception, e:
      raise e

  def create(self, data, db, cursor):
    sql = "INSERT INTO photos(fb_id, filename, caption, \
           owner_id, state, created_at) \
           VALUES ('%s', '%s', '%s', '%d', '%s', '%d')" % \
           (data[0], data[1], data[2], data[3], data[4], \
            data[5])

    try:
      cursor.execute(sql)

      db.commit() # commit changes

      id = cursor.lastrowid

      self.load_from_tuple((id,) + data)
    except Exception, e:
      db.rollback()
      raise e

  def set_state(self, new_state):
    self.data['state'] = new_state

  def save(self, cursor, db):

    sql = "UPDATE photos SET fb_id = '%s', filename = '%s', caption = '%s', \
           owner_id = '%d', state = '%s', created_at = '%d' \
           WHERE id = '%d'" % \
           (self.data['fb_id'], self.data['filename'], self.data['caption'], \
            self.data['owner_id'], self.data['state'], self.data['created_at'], \
            self.data['id'])

    try:
      cursor.execute(sql)

      db.commit() # commit changes
    except Exception, e:
      db.rollback()
      raise e

  def like(self, data, db, cursor):
    sql = "INSERT INTO likes(photo_id, user_id, created_at) \
           VALUES ('%d', '%d', '%d')" % \
           (self.data['id'], data['user_id'], data['created_at'])

    try:
      cursor.execute(sql)

      db.commit() # commit changes
    except Exception, e:
      db.rollback()
      raise e

  def unlike(self, user_id, db, cursor):
    sql = "DELETE FROM likes \
           WHERE photo_id = '%d' AND user_id = '%d'" % \
           (self.data['id'], user_id)

    try:
      cursor.execute(sql)

      db.commit() # commit changes
    except Exception, e:
      db.rollback()
      raise e

  def check_like(self, user_id, db, cursor):
    sql = "SELECT id FROM likes \
           WHERE photo_id = '%d' AND user_id = '%d'" % \
           (self.data['id'], user_id)

    try:
      cursor.execute(sql)
      data = cursor.fetchone()
      if data = None:
        return False

    except Exception, e:
      db.rollback()
      raise e

    return True

  def load_from_tuple(self, data):
    self.data['id'] = data[0]
    self.data['fb_id'] = data[1]
    self.data['filename'] = data[2]
    self.data['caption'] = data[3]
    self.data['owner_id'] = data[4]
    self.data['state'] = data[5]
    self.data['created_at'] = data[6]
