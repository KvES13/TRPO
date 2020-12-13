from app import db
from datetime import datetime


# >>> from app import db
# >>> db.create_all()

class DFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(30), nullable=False)
    filepath = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<DFile %r>' % self.id


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Statistics %r>' % self.id
