#Snaps

The backend for snaps - a platform for sharing photos

##Dev Setup

* Clone repo
* Install dependencies using `virtualenv`
* Load database schema and modify database credentials
* Start server with `python app.py`

##Architecture

MVC architecture with an additional Services layer to separate application logic

 * Interfacing through routes (present in the file `app.py`)
 * Controllers associated with each route (present in the file `app.py`)
 * Services to contain all application logic
 * Models as data layer

##Endpoints

###POST /photos/new

Upload a new photo

####Parameters
 * `user_id` - user identifier
 * `caption` - photo caption
 * `access_token` - facebook access token to verify user
 * `photo` - the photo

####Sample Response
```json
{"action_performed": "photo.upload", "action_status": true}
```

###GET /photos

Fetch list of photos based on **time** or **likes**

####Parameters
 * `sort_by` - possible values are `time` and `like`
 * `after` - load photos after this timestamp (only when `sort_by` is set to `time`)
 * `before` - load photos before this timestamp (only when `sort_by` is set to `time`)
 * `photo_id` - returns photos with likes less than or equal to this photo and uploaded before it (only used when `sort_by` is set to `like`)

####Sample Response
```json
{"data": [
  {
    "url": "http://localhost:5000/static/imgs/camping.png",
    "caption": "Camping trip to Antargange",
    "likes_count": 5,
    "owner": {
      "id": 2,
      "name": "Abhishek Kandoi",
      "profile_pic": "http://localhost:5000/static/imgs/kandoi.png"
    }
  },
  {
    "url": "http://localhost:5000/static/imgs/trekking.png",
    "caption": "spelunking and trekking at Antargange",
    "likes_count": 12,
    "owner": {
      "id": 2,
      "name": "Abhishek Kandoi",
      "profile_pic": "http://localhost:5000/static/imgs/kandoi.png"
    }
  }
]}
```

###POST /users/new

Create a new user

####Parameters
 * `access_token` - facebook access token

####Sample Response
```json
{"action_status": true}
```

###POST /photos/mark

Mark a photo as **reviewed** or **disallow** (_admin only for now_)

####Parameters
 * `photo_id` - photo identifier
 * `mark_as` - new state of photo (TODO: should be chosen from a discrete set in future)

####Sample Response
```json
{"action_status": true}
```

###POST /photos/toggle_like

Toggle the like state of a photo

####Parameters
 * `photo_id` - photo identifier
 * `access_token` - facebook access token
 * `user_id` - user identifier

####Sample Response
```json
{"action_performed": "photo.unlike", "action_status": true}
```
