from app.models import User,Post, Comment,Clap
from app import db

# def setUp(self):
#     self.user_Jack = User(username = 'Jack',password = 'vila', email = 'jackotienokey@gmail.com')
    
def tearDown(self):
        Post.query.delete()
        User.query.delete()
        Comment.query.delete()
        Clap.query.delete()