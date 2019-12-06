consumer_key1 = 'oBrLD7TXcwIMFRbXp3oKNFfUD'
consumer_secret1 = 'ZGsyth8fyZzv32s366kaf0fL8QKchpOnV9VswjsGj4DAllZrnr'

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "verysecretkey"

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True