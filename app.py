import json

from flask import Flask, render_template, url_for, request, make_response, Response


app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage_display():
  return render_template('landing_page.html')

@app.route('/photos', methods=['GET'])
def photo_list_fetch():
  offset = request.args.get('offset', '')

  return Response(json.dumps({"data": [{"photo_id":"5"}, {"photo_id": "6"}]}),
                  mimetype='application/json')

if __name__ == '__main__':
  app.run(debug=True)