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
    sql = "INSERT INTO photos(id, fb_id, filename, caption, \
           owner_id, state, created_at) \
           VALUES ('%d', '%s', '%s', '%s', '%d', '%s', '%d')" % \
           (data[0], data[1], data[2], data[3], data[4], \
            data[5], data[6])

    try:
      cursor.execute(sql)

      db.commit() # commit changes

      self.load_from_tuple(data)
    except Exception, e:
      db.rollback()
      raise e
  def set_state(self, new_state):
    self.data['state'] = new_state

  def load_from_tuple(self, data):
    self.data['id'] = data[0]
    self.data['fb_id'] = data[1]
    self.data['filename'] = data[2]
    self.data['caption'] = data[3]
    self.data['owner_id'] = data[4]
    self.data['state'] = data[5]
    self.data['created_at'] = data[6]
