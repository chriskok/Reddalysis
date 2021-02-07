import datetime

from mongoengine import *
db = connect('mongoengine_test', host='localhost', port=27017)
db.drop_database('mongoengine_test')

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50, unique=True)
    last_name = StringField(max_length=50)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)

    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class LinkPost(Post):
    link_url = StringField()

user_1 = User(
    email='hulu@hulu.com',
    first_name='mr',
    last_name='hulu'
).save()

post_1 = Post(
    title='Sample Post',
    author=user_1
)

post_1.save()       # This will perform an insert
print(post_1.title)
post_1.title = 'A Better Post Title'
post_1.save()       # This will perform an atomic edit on "title"
print(post_1.title)

user_2 = User(
    email='yahoo@yahoo.com',
    first_name='ms',
    last_name='yahoo'
)
user_2.save()

post_2 = Post(
    title='Random Post',
    author=user_2
).save()

for post in Post.objects:
    print(post.title)

user_obj = User.objects(first_name='mr')

for curr_user in user_obj:
    print(curr_user.last_name)
