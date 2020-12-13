from werkzeug.utils import secure_filename
import os
from app import db
import pymorphy2 as py
import re
import string
import io

source = '''
Вася ест кашу
# сущ  гл  сущ
# что/кто  делает с_чем-то
NOUN,nomn VERB NOUN,accs

Красивый цветок
ADJF NOUN

Птица сидит на крыше
# сущ  гл  предлог сущ
NOUN,nomn VERB NOUN,loct
'''


MAX_FILE_SIZE = 10 * (1024 * 1024) + 1
ALLOWED_EXTENSIONS = {'txt', 'docx'}

subject = ("NOUN", "NPRO")
subject_cases = "nomn"
predicate = ("VERB", "INFN", "GRND")
addition = ("NUMR", )
attribute = ("ADJF", "ADJS", "PRTF")
adverbial_modifier = ("COMP", "ADVB", "PRED")
rest = ("PREP", "CONJ", "PRCL", "INTJ")


class FileContent(object):
    def __init__(self, filename, filepath, date):
        self.__filename = filename
        self.__filepath = filepath
        self.__date = date


    def getFileText(self):
        with open(self.__filepath, encoding="utf8") as f:
            text = f.read()
            return text
        return "ERROR"


    def getFName(self):
        return self.__filename


    def getDate(self):
        return self.__date.date()


    def getFPath(self):
        return self.__filepath


class Analyzer(object):

    words_count = 0

    def __init__(self, text):
        self.text = text
        self.stat = {"Подлежащее": 0, "Сказуемое": 0, "Дополнение": 0,
                     "Определение": 0, "Обстоятельство": 0, "Остатки": 0}
        # self.patterns = parseSource(source)
        self.ultra_mega_algo()

    def calculateWordsCount(self):
        words = self.text.split()
        self.words_count = len(words)
        print(self.words_count)
        return self.words_count


    def getText(self):
        # parseText(self.patterns, self.text)
        return self.text

    def getDict(self):
        return self.stat


    def ultra_mega_algo(self):
        split_regex = re.compile(r'[.|!|?|…]')
        sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(self.text)])
        for s in sentences:
            morph = py.MorphAnalyzer()
            words = s.split()
            for word in words:

                word = word.strip(string.punctuation)
                p = morph.parse(word)[0]
                if p.tag.POS in subject:
                    if p.tag.case == subject_cases:
                        self.stat["Подлежащее"] += 1
                elif p.tag.POS in predicate:
                    self.stat["Сказуемое"] += 1
                elif p.tag.POS in addition:
                    self.stat["Дополнение"] += 1
                elif p.tag.POS in attribute:
                    self.stat["Определение"] += 1
                elif p.tag.POS in subject:
                    self.stat["Обстоятельство"] += 1
                else:
                    self.stat["Остатки"] += 1
                # self.calculateWordsCount(p.tag.POS)
                print(p.tag.POS, word)
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
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



