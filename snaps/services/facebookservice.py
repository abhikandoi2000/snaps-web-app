import facebook

class FacebookService:
  def __init__(self, access_token):
    self.graph = facebook.GraphAPI(access_token)

  def fetch_all_photos(self):
    photos_list = []

    me = self.graph.get_object(id='me')

    photos = self.graph.get_connections(id='me', connection_name='photos', limit=500)

    for photo in photos['data']:
      if photo['from']['id'] == me['id']:
        largest_image = photo['images'][0]
        caption = photo.get('name', '')

        photos_list.append({
              "id": photo['id'],
              "src": largest_image['source'],
              "height": largest_image['height'],
              "width": largest_image['width'],
              "caption": caption
            })

    return photos_list

  def fetch_profile_pic(self):
    profile_pic = self.graph.get_connections(id='me', connection_name='picture')

    return profile_pic['url']
