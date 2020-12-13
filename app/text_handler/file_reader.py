from werkzeug.utils import secure_filename
import os
from app import db

MAX_FILE_SIZE = 10 * (1024 * 1024) + 1
ALLOWED_EXTENSIONS = {'txt', 'docx'}


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


