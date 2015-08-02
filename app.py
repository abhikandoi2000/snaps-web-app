from flask import Flask, render_template, url_for, request
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def homepage_display():
  return render_template('landing_page.html')

if __name__ == '__main__':
  app.run(debug=True)