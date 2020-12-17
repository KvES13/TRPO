from app import db, models
from sqlalchemy import text
from app.models import WordsList, Statistics, Words
import re
from collections import defaultdict


def get_sentences(f_id, sentences_type, key):
    query = text("SELECT text FROM Sentences where file_id = :f_id ")
    res = db.engine.execute(query, f_id=f_id)
    file_text = ""
    w_dict = make_words_dict(f_id, sentences_type, key)
    sentences_number = 1
    print(w_dict)
    for row in res:
        if sentences_number in w_dict:
            file_text += add_color(row[0], w_dict.get(sentences_number))
        else:
            file_text += row[0]
        sentences_number += 1
    return file_text


def make_words_dict(f_id, sentences_type, key):
    words_dict = {}
    if key == "":
        records = db.session.query(WordsList.sentence_id,
                                   WordsList.word_num).filter(WordsList.file_id == f_id,
                                                           WordsList.role == sentences_type).all()
    else:
        word_id = db.session.query(Words.id).filter(Words.word == key).first()
        if word_id is None:
            return words_dict
        records = db.session.query(WordsList.sentence_id,
                                   WordsList.word_num).filter(WordsList.file_id == f_id,
                                                              WordsList.role == sentences_type,
                                                              WordsList.word_id == word_id[0]).all()


    for rec in records:
        if rec.sentence_id in words_dict:
            words_dict[rec.sentence_id].append(rec.word_num)
        else:
            words_dict[rec.sentence_id] = [rec.word_num]

    print(words_dict)
    return words_dict


def add_color(sentence, words_numbers):
    fields = sentence.split()
    print(words_numbers)
    for ind in words_numbers:
        print(ind, "                 ind")
        fields[ind-1] = '<a class="bg-info text-white">' + fields[ind-1] + '</a>'

    s = ' '.join(fields)
    return s


def get_file_stat(f_id):
    return db.session.query(Statistics).filter(Statistics.parent_id == f_id).first()


def save_file_stat(f_id, stat_list):
    print("")


def get_file_info(id):
    return models.Files.query.get(id)
