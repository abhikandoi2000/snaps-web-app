from flask import Flask
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def homepage_display():
  return 'Authentic experiences of people you know!'

if __name__ == '__main__':
  app.run(debug=True)