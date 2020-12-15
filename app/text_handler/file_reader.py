from werkzeug.utils import secure_filename
import pymorphy2 as py
import re
import string



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
                     "Определение": 0, "Обстоятельство": 0, "Неизвестно": 0}
        # self.patterns = parseSource(source)
        self.ultra_mega_algo()
        self.words_count = self.calculateWordsCount()

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

    def getWordsCount(self):
        return self.words_count

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
                    else:
                        self.stat["Дополнение"] += 1
                elif p.tag.POS in addition or p.tag.POS in rest:
                    self.stat["Дополнение"] += 1

                elif p.tag.POS in predicate:
                    self.stat["Сказуемое"] += 1
                elif p.tag.POS in attribute:
                    self.stat["Определение"] += 1
                elif p.tag.POS in adverbial_modifier:
                    self.stat["Обстоятельство"] += 1
                else:
                    self.stat["Неизвестно"] += 1


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



