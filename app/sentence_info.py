from enum import Enum
from  dataclasses import dataclass

subject = ("NOUN", "NPRO")
subject_case = 'nomn'
predicate = ("VERB", "INFN", "GRND")
addition = "NUMR"
attribute = ("ADJF", "ADJS", "PRTF")
adverbial_modifier = ("COMP", "ADVB", "PRED")
rest = ("PREP", "CONJ", "PRCL", "INTJ")


parts = ("Все", "Подлежащее", "Сказуемое", "Дополнение",
         "Определение", "Обстоятельство", "Неизвестно")


class SParts(Enum):
    all = 0
    subject = 1
    predicate = 2
    addition = 3
    attribute = 4
    adverbial_modifier = 5
    unknown = 6


@dataclass
class Context(object):
    filename: str
    filepath: str
    words_count: int
    key_word: str
    key_type: int