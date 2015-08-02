import MySQLdb
import json

class User:
  def __init__(self):
    self.data = {
      "id": None,
      "name": None,
      "uid": None,
      "provider": None,
      "credentials": None,
      "email": None,
      "created_at": None,
      "updated_at": None
    }

  def load_from_db(self, user_id, cursor):
    sql = "SELECT id, name, uid, provider, credentials, email, created_at, updated_at \
           FROM users \
           WHERE id = %d" % user_id

    try:
      cursor.execute(sql)
      data = cursor.fetchone()

      self.load_from_tuple(data)

      return "Hello"
    except Exception, e:
      raise e

  def create(self, data, db, cursor):
    sql = "INSERT INTO users(name, uid, provider, \
           credentials, email, created_at, updated_at) \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%d', '%d')" % \
           (data[0], data[1], data[2], data[3], data[4], \
            data[5], data[6])

    try:
      cursor.execute(sql)

      db.commit() # commit changes

      id = cursor.lastrowid

      self.load_from_tuple((id,) + data)
    except Exception, e:
      db.rollback()
      raise e

  def verify_creds(self, access_token, cursor, db):
    sql = "SELECT credentials \
           FROM users \
           WHERE id = %d" % self.data['id']

    try:
      cursor.execute(sql)
      data = cursor.fetchone()

      credentials = json.loads(data[0])
      token = credentials["token"]

      if token == access_token:
        return True

      print credentials
    except Exception, e:
      raise e

    return False

  def load_from_tuple(self, data):
    self.data['id'] = data[0]
    self.data['name'] = data[1]
    self.data['uid'] = data[2]
    self.data['provider'] = data[3]
    self.data['credentials'] = data[4]
    self.data['email'] = data[5]
    self.data['created_at'] = data[6]
    self.data['updated_at'] = data[7]