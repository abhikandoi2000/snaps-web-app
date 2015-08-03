import requests

class FileUtility:
  def __init__(self):
    pass

  def download(self, url, filepath):
    r = requests.get(url, stream = True)

    if r.status_code == 200:
      with open(filepath, 'wb') as outfile:
        for chunk in r.iter_content(1024):
          outfile.write(chunk)
