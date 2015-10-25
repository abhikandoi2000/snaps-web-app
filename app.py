import json
import shutil
from os import getcwd, path
import time

from flask import Flask, render_template, url_for, request, make_response, Response
from werkzeug import secure_filename
import MySQLdb
from PIL import Image

from snaps.models.user import User
from snaps.models.photo import Photo
from snaps.models.photolist import PhotoList
from snaps.services.photoservice import PhotoService
from snaps.services.facebookservice import FacebookService
from snaps.services.userservice import UserService
from snaps.utilities.imageutility import ImageUtility
from snaps.utilities.fileutility import FileUtility

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

  return render_template('landing_page.html')

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

@app.route('/users/new/', methods=['POST'])
def user_create():
  access_token = request.form['access_token']

  # TODO: check for an existing user here

  fb_service = FacebookService(access_token)
  user_details = fb_service.fetch_details()
  name = user_details['name']
  uid = user_details['id']
  email = "need_to@fixthis.com" # TODO: fetch this using the fb service
  photos = fb_service.fetch_all_photos()

  # save the user to db
  user_service = UserService()
  # TODO: fix the field expires
  user_id = user_service.create(name, uid, email, {"token": access_token, "expires": "never"}, db, cursor)
  user_id = int(user_id)


  file_service = FileUtility()
  photo_service = PhotoService()
  image_utility = ImageUtility()

  for photo in photos:
    extension = "jpg" # TODO: extract proper file extension here

    filepath = path.join(getcwd(), "static/original/" + photo['id'] + "." + extension)
    file_service.download(photo['src'],
      filepath
      )

    # copy,crop and save photo
    copy_filepath = path.join(getcwd(), "static/cropped/" + photo['id'] + "." + extension)
    original = Image.open(filepath)

    cropped = image_utility.crop(original)
    cropped.save(copy_filepath)

    photo_service.insert_into_db({
        'fb_id': photo['id'],
        'filename': photo['id'] + "." + extension,
        'caption': photo['caption'],
        'owner_id': user_id
      }, db, cursor)

  return Response(json.dumps({"action_status": True}),
      mimetype='application/json')

@app.route('/photos/', methods=['GET'])
def photolist_fetch():
  sort_by = request.args.get('sort_by', 'time')

  photo_service = PhotoService()
  if sort_by == 'time':
    intime = 'after'
    timestamp = int(request.args.get('after', 0))

    if timestamp == 0:
      intime = 'before'
      timestamp = int(request.args.get('before', int(time.time())))

    photos = photo_service.fetch_by_time(db, cursor, intime, timestamp)
  else:
    # TODO: set the default properly
    photo_id = request.args.get('photo_id', None)
    if photo_id:
      photo_id = int(photo_id)
      photos = photo_service.fetch_by_likes(db, cursor, photo_id)
    else:
      photos = photo_service.fetch_all_photos_by_likes(db, cursor)

  return Response(json.dumps({"data": photos}), mimetype='application/json')

@app.route('/photos/mark/', methods=['POST'])
def photo_mark():
  photo_id = int(request.form['photo_id'])
  mark_as = request.form['mark_as']

  photo_service = PhotoService()
  photo_service.change_state(photo_id, mark_as, db, cursor)

  return Response(json.dumps({"action_status": True}),
      mimetype='application/json')

@app.route('/photos/toggle_like/', methods=['POST'])
def photo_like_toggle():
  photo_id = int(request.form['photo_id'])
  access_token = request.form['access_token']
  user_id = int(request.form['user_id'])

  photo_service = PhotoService()
  resp_dict = photo_service.toggle_like(photo_id, user_id, access_token, db, cursor)

  return Response(json.dumps(resp_dict),
      mimetype='application/json')

if __name__ == '__main__':
  app.run(debug=True)

  # disconnect from server
  db.close()

