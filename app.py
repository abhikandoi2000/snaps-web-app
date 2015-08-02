import json

from flask import Flask, render_template, url_for, request, make_response, Response
import MySQLdb

from snaps.models.user import User
from snaps.models.photo import Photo

app = Flask(__name__)

# Open database connection
db = MySQLdb.connect("localhost","sdslabs","try123","snaps")

# prepare a cursor object using cursor() method
cursor = db.cursor()

@app.route('/', methods=['GET'])
def homepage_display():
  photo = Photo()
  # photo.load_from_db(1, cursor)
  photo.create((2, "2222222", "2222222.png", "But I was never meant to do this!", 5, "unreviewed", 2222222), db, cursor)
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
