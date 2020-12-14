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
    parent_id = db.Column(db.Integer,  nullable=False)
    words_count = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.Integer, nullable=False)
    predicate = db.Column(db.Integer, nullable=False)
    addition = db.Column(db.Integer, nullable=False)
    attribute = db.Column(db.Integer, nullable=False)
    adverbial_modifier = db.Column(db.Integer, nullable=False)
    unknown = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Statistics %r>' % self.id
