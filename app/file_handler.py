import pymorphy2 as py
import re
import string
import docx

from app import models, db, sentence_info as si

MAX_FILE_SIZE = (1024 * 1024) + 1
ALLOWED_EXTENSIONS = {'txt', 'docx'}


def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return filename.rsplit('.', 1)[1]
    else:
        return "undef"


def read_from_file(filepath, file_format):
    print(filepath, " ############",file_format)
    if file_format == 'txt':
        print("#################Y TTTTTTTTXXXXXXXXXXTTTTTTTTTT")
        with open(filepath, "r", encoding="utf8") as f:
            text = f.read()
            return text
    elif file_format == 'docx':
        doc = docx.Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text

    else:
        return "ERROR"


class Analyzer(object):
    words_count = 0

    def __init__(self, id):
        self.text_id = id
        self.words_count = 0

    def calculateWordsCount(self, text):
        words = text.split()
        return len(words)

    def getText(self):
        # parseText(self.patterns, self.text)
        return self.text

    def getDict(self):
        return self.stat

    def getWordsCount(self):
        return self.words_count

    def ultra_mega_algo(self, text):
        self.words_count = self.calculateWordsCount(text)
        stat = {si.SParts.subject: 0, si.SParts.predicate: 0, si.SParts.addition: 0,
                si.SParts.attribute: 0, si.SParts.adverbial_modifier: 0, si.SParts.unknown: 0}
        split_regex = re.compile(r'[.|!|?|…]')
        sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(text)])
        morph = py.MorphAnalyzer()
        counter = 1
        unique_words = {}
        word_records_list = []
        words_list = []
        word_index = models.Words.query.count()

        for s in sentences:
            word_counter = 1
            for word in s.split():
                word = word.strip(string.punctuation).lower()
                p = morph.parse(word)[0]
                if p.tag.POS in si.subject:
                    if p.tag.case == si.subject_case:
                        part = si.SParts.subject
                        stat[part] += 1
                    else:
                        part = si.SParts.addition
                        stat[part] += 1
                elif p.tag.POS == si.addition or p.tag.POS in si.rest:
                    part = si.SParts.addition
                    stat[part] += 1
                elif p.tag.POS in si.predicate:
                    part = si.SParts.predicate
                    stat[part] += 1
                elif p.tag.POS in si.attribute:
                    part = si.SParts.attribute
                    stat[part] += 1
                elif p.tag.POS in si.adverbial_modifier:
                    part = si.SParts.adverbial_modifier
                    stat[part] += 1
                else:
                    part = si.SParts.unknown
                    stat[part] += 1

                if word not in unique_words:
                    ind = models.Words.query.get(word)
                    if ind:
                        # Кривые индексы
                        unique_words[word] = ind.id
                    else:
                        ind = models.Words.query.count()
                        if ind != 0:
                            unique_words[word] = ind + word_counter
                        else:
                            unique_words[word] = word_counter

                    u_word_record = models.Words(word=word)
                    words_list.append(u_word_record)
                    # word_index += 1
                role = int(part.value)
                sentence_record = models.Sentences(file_id=self.text_id, number=counter, text=s)
                word_record = models.WordsList(file_id=self.text_id, sentence_id=counter,
                                               word_id=unique_words.get(word), word_num=word_counter, role=role)
                word_records_list.append(word_record)
                word_counter += 1
            db.session.add(sentence_record)
            db.session.commit()
            for el in words_list:
                db.session.add(el)
            db.session.commit()
            for el in word_records_list:
                db.session.add(el)
            db.session.commit()
            counter += 1
        words_list.clear()
        word_records_list.clear()
        # u_word_record.clear()
        # TO
        # DO Перенести в другой файл
        rec = models.Statistics(parent_id=self.text_id, words_count=self.words_count,
                                subject=stat.get(si.SParts.subject), predicate=stat.get(si.SParts.predicate),
                                addition=stat.get(si.SParts.addition), attribute=stat.get(si.SParts.attribute),
                                adverbial_modifier=stat.get(si.SParts.adverbial_modifier),
                                unknown=stat.get(si.SParts.unknown))
        db.session.add(rec)
        db.session.commit()

        # print(unique_words)


