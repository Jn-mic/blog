from app.models import User,Post, Comment,Clap
from app import db

def setUp(self):
    self.user_Jack = User(username = 'Jack',password = 'vila', email = 'jackotienokey@gmail.com')
    # self.new_user = Review(movie_id=12345,movie_title='Review for movies',image_path="#",movie_review='T',user = self.user_Jack )

def tearDown(self):
        Post.query.delete()
        User.query.delete()
        Comment.query.delete()
        Clap.query.delete()