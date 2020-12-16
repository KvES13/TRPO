from werkzeug.utils import secure_filename
import pymorphy2 as py
import re
import string
import docx
from app import models,db
from enum import Enum

MAX_FILE_SIZE = (1024 * 1024) + 1

subject = ("NOUN", "NPRO")
subject_cases = 'nomn'
predicate = ("VERB", "INFN", "GRND")
addition = ("NUMR",)
attribute = ("ADJF", "ADJS", "PRTF")
adverbial_modifier = ("COMP", "ADVB", "PRED")
rest = ("PREP", "CONJ", "PRCL", "INTJ")

sentence_part = ("Подлежащее", "Сказуемое", "Дополнение",
                 "Определение", "Обстоятельство", "Неизвестно")


class FileContent(object):
    def __init__(self, filename, filepath, date, fileformat):
        self.__filename = filename
        self.__filepath = filepath
        self.__date = date
        self.__format = fileformat

    def getFileText(self):
        if self.__format == 'txt':
            with open(self.__filepath, "r", encoding="utf8") as f:
                text = f.read()
                return text
        elif self.__format == 'docx':
            doc = docx.Document(self.__filepath)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            return text

        return "ERROR"

    def getFName(self):
        return self.__filename

    def getDate(self):
        return self.__date.date()

    def getFPath(self):
        return self.__filepath

    def getFormat(self):
        return self.__format


class Analyzer(object):
    words_count = 0

    def __init__(self, id, text):
        self.text = text
        self.stat = {sentence_part[0]: 0, sentence_part[1]: 0, sentence_part[2]: 0,
                     sentence_part[3]: 0, sentence_part[4]: 0, sentence_part[5]: 0}
        self.text_id = id
        # self.patterns = parseSource(source)
        self.words_count = self.calculateWordsCount()

    def calculateWordsCount(self):
        words = self.text.split()
        self.words_count = len(words)
        print(self.words_count, "words count ************", words)
        return self.words_count

    def getText(self):
        # parseText(self.patterns, self.text)
        return self.text

    def getDict(self):
        return self.stat

    def getWordsCount(self):
        return self.words_count

    def ultra_mega_algo(self):
        split_regex = re.compile(r'[.|!|?|…]')
        sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(self.text)])
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
                if p.tag.POS in subject:
                    if p.tag.case == subject_cases:
                        self.stat["Подлежащее"] += 1
                        role = 0
                    else:
                        self.stat["Дополнение"] += 1
                        role = 2
                elif p.tag.POS in addition or p.tag.POS in rest:
                    self.stat["Дополнение"] += 1
                    role = 2
                elif p.tag.POS in predicate:
                    self.stat["Сказуемое"] += 1
                    role = 1
                elif p.tag.POS in attribute:
                    self.stat["Определение"] += 1
                    role = 3
                elif p.tag.POS in adverbial_modifier:
                    self.stat["Обстоятельство"] += 1
                    role = 4
                else:
                    self.stat["Неизвестно"] += 1
                    role = 5

                if word not in unique_words:
                    ind = models.Words.query.get(word)
                    if ind:
                        #Кривые индексы
                        unique_words[word] = ind.id
                        print(ind, "            ind id ")
                        print(ind.id, "            ind id ")
                    else:
                        ind = models.Words.query.count()
                        print(ind, "          count   ind id ")
                        if ind != 0:
                            unique_words[word] = ind+word_counter
                            print(word_counter, "          wcccccccc ",ind)
                        else:
                            unique_words[word] = word_counter
                            print(word_counter, "          wcccccccc ")

                    u_word_record = models.Words(word=word)
                    words_list.append(u_word_record)
                    # word_index += 1
                    # print(word_index)

                sentence_record = models.Sentences(file_id=self.text_id, id=counter, text=s)
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
        print(unique_words)

    # def calculate_sentence_part(self,speech_part):
    #     if speech_part == "NOUN"

    #  def parseLine():
    #     was = False
    #     for p in pats:
    #         res = p
    #         .checkPhrase(line)
    #         if res:
    #             print('+', line, p.tags, [r[0] for r in res])
    #             was = True
    #     if not was:
    #         print('-', line)
    #
    # buf = io.StringIO(text)
    # s = buf.readline()
    # while s:
    #     s = s.strip()
    #     if s != '':
    #         parseLine(s)
    #     s = buf.readline()


def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1] == 'txt':
        return 'txt'
    elif '.' in filename and filename.rsplit('.', 1)[1] == 'docx':
        return 'docx'
    else:
        return 'undef'
