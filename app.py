import json

from flask import Flask, render_template, url_for, request, make_response, Response
from werkzeug import secure_filename
from os import getcwd, path
import MySQLdb
from PIL import Image

from snaps.models.user import User
from snaps.models.photo import Photo
from snaps.models.photolist import PhotoList
from snaps.services.photoservice import PhotoService
from snaps.services.userservice import UserService
from snaps.utilities.imageutility import ImageUtility

ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']

app = Flask(__name__)

# Open database connection
db = MySQLdb.connect("localhost","sdslabs","try123","snaps")

# prepare a cursor object using cursor() method
cursor = db.cursor()

def allowed_file(filename):
  return '.' in filename and \
          filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def homepage_display():
  # image_utility = ImageUtility()
  # photo = Image.open(path.join(getcwd(), "static/original/cousin.jpg"))
  # cropped_photo = image_utility.crop(photo)
  # cropped_photo.save(path.join(getcwd(), "static/cropped/cousin.jpg"), optimize=True, quality=60)

  # user_service = UserService()
  # user_service.create("Adam Levine", "777777777", "i@adamlevin.com", {"access_token": "jlkSLAJD0aisdAS09da=", "expires": "143345446"}, db, cursor)
  # photo_service = PhotoService()
  # photo_service.insert_into_db({"fb_id": "66666666", "filename": "66666666.jpg", ""}, db, cursor)
  # photo_service.change_state(2, 'launched', db, cursor)
  # photo_service.toggle_like(2, 6, "aNJKJHsdakdaNAKsdhkJHdanashdLDSnlja=", db, cursor)
  # print photo_service.fetch_list(cursor, 0)

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

@app.route('/photos/', methods=['GET'])
def photo_list_fetch():
  offset = request.args.get('offset', '')

  return Response(json.dumps({"data": [{"photo_id":"5"}, {"photo_id": "6"}]}),
                  mimetype='application/json')

@app.route('/photos/new/', methods=['POST'])
def photo_upload():
  user_id = int(request.form['user_id'])
  caption = request.form['caption']
  access_token = request.form['access_token']

  photo = request.files['photo']

  if photo and allowed_file(photo.filename):
    filename = secure_filename(photo.filename)
    print filename

    photo_service = PhotoService()
    try:
      return Response(json.dumps(
          photo_service.upload(photo, filename, \
                               user_id, caption, access_token, db, cursor)
        ), mimetype='application/json')
    except Exception, e:
      raise e

if __name__ == '__main__':
  app.run(debug=True)

  # disconnect from server
  db.close()
