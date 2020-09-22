from app import db 


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    about = db.Column(db.Text)
    email = db.Column(db.String, unique=True)


    @property 
    def is_authenticated(self):
        return True 
    
    @property
    def is_active(self):
        return True

    @property 
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

        

    def __init__(self, username, password, name, email, about):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.about = about

    def __repr__(self):
        return "<User %r>" % self.username


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    title = db.Column(db.String)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    user = db.relationship('User', foreign_keys=user_id)

    def __ini__(self, content, title, date, user_id):
        self.content = content
        self.title = title 
        self.date = date
        self.user_id = user_id

    def __repr__(self):
        return "<Post %r>"


class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)
    follower = db.relationship('User', foreign_keys=follower_id)