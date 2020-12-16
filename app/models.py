from app import db
from datetime import datetime


# >>> from app import db
# >>> db.create_all()

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(30), nullable=False)
    filepath = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

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

    create_fields = update_fields = ['parent_id', 'words_count', 'subject', 'predicate',
                                     'addition', 'attribute', 'adverbial_modifier', 'unknown']

    def __repr__(self):
        return '<Statistics %r>' % self.id


class Sentences(db.Model):
    # file_id = db.Column(db.Integer, db.ForeignKey('files.id'), primary_key=True)
    file_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer,  primary_key=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Sentences {self.text}>'


class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Words {self.word}>'


class WordsList(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer,  primary_key=True)
    word_id = db.Column(db.Integer )
    # file_id = db.Column(db.Integer, db.ForeignKey('files.id'), primary_key=True)
    # sentence_id = db.Column(db.Integer, db.ForeignKey('sentences.id'), primary_key=True)
    # word_id = db.Column(db.Integer, db.ForeignKey('words.id'))
    word_num = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<WordsList {self.role}>'
