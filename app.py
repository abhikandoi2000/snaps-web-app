import json

from flask import Flask, render_template, url_for, request, make_response, Response
import MySQLdb

from snaps.models.user import User
from snaps.models.photo import Photo
from snaps.models.photolist import PhotoList
from snaps.services.photoservice import PhotoService

app = Flask(__name__)

# Open database connection
db = MySQLdb.connect("localhost","sdslabs","try123","snaps")

# prepare a cursor object using cursor() method
cursor = db.cursor()

@app.route('/', methods=['GET'])
def homepage_display():
  photo_service = PhotoService()
  # photo_service.insert_into_db({"fb_id": "66666666", "filename": "66666666.jpg", ""}, db, cursor)
  # photo_service.change_state(2, 'launched', db, cursor)
  # photo_service.toggle_like(2, 6, "aNJKJHsdakdaNAKsdhkJHdanashdLDSnlja=", db, cursor)

  # photo = Photo()
  # photo.load_from_db(3, cursor)
  # photo.create(("3333333", "3333333.png", "Did this and that but never all at once!", 3, "unreviewed", 33333333), db, cursor)
  # photo.set_state("launched")
  # photo.save(cursor, db)
  # photo.like({"user_id": 2, "created_at": 555555}, db, cursor)
  # photo.unlike(2, db, cursor)
  # photo.check_like(4, db, cursor)
  # list = PhotoList()
  # photos = list.load(0, 10, cursor)
  # print photos

  # user = User()
  # user.create(("Nupur Bothra", "1", "Facebook",
  #              json.dumps({
  #                   "token": "aNJKJHsdakdaNAKsdhkJHdanashdLDSnlja=",
  #                   "expires": "never"
  #                 }),
  #              "nupurbothra@gmail.com", 12121212, 12121212), db, cursor)

  # user = User()
  # user.load_from_db(6, cursor)
  # print user.verify_creds("aNJKJHsdakdaNAKsdhkJHdanashdLDSnlja=", cursor, db)

  return render_template('landing_page.html')

@app.route('/photos', methods=['GET'])
def photo_list_fetch():
  offset = request.args.get('offset', '')

  return Response(json.dumps({"data": [{"photo_id":"5"}, {"photo_id": "6"}]}),
                  mimetype='application/json')

if __name__ == '__main__':
  app.run(debug=True)

  # disconnect from server
  db.close()
