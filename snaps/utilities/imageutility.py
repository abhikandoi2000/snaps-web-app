from PIL import Image

class ImageUtility:
  def __init__(self):
    pass

  def crop(self, photo):
    width, height = photo.size

    if width > height:
      delta = width - height

      left = int(delta/2)
      right = left + height

      upper = 0
      lower = height

      photo = photo.crop((left, upper, right, lower))
    elif height > width:
      delta = height - width

      left = 0
      right = width

      upper = int(delta/2)
      lower = width + upper

      photo = photo.crop((left, upper, right, lower))

    return photo

    def resize(self, photo, new_size):
      photo.thumbnail(new_size, Image.ANTIALIAS)

      return photo