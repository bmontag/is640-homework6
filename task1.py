import string
from collections import Counter

FILE_PATH = "hw.txt"
OUTPUT_PATH = "summary.txt"

TOTAL_WORD_COUNT = "Total word count: {}"
TOTAL_CHARACTER_COUNT = "Total character count: {}"
AVERAGE_WORD_LENGTH = "The average word length: {:.2f}"
AVERAGE_SENTENCE_LENGTH = "The average sentence length: {:.2f}"
LY_WORDS_DISTRIBUTION = "\nA word distribution of all words ending in \"ly\":"
WORD_DISTRIBUTION = "{}: {}"
DESC_LONGEST_WORD = "\nA list of top 10 longest words in descending order:"

ALL_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

class WordAnalysis():
    raw_data = ""
    words = []
    sanitized_words = []
    word_count = 0
    character_count = 0
    # average_word_length = 0
    # average_sentence_length = 0

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.parse_raw_data()
        self.sanitize_words()

    def parse_raw_data(self):
        line_delimiter = "\n"
        item_delimiter = " "
    
        lines = self.raw_data.split(line_delimiter)

        for line in lines:
            self.character_count += len(line)

            chunks = line.split(item_delimiter)
            while "" in chunks:
                chunks.remove("")

            if len(chunks) == 0:
                continue

            self.words += chunks
            self.word_count += len(chunks)

    def sanitize_words(self):
        for word in self.words:
            s_word = word.lstrip(string.punctuation)
            s_word = s_word.rstrip(string.punctuation)
            self.sanitized_words.append(s_word.capitalize()) 

    def average_word_length(self):
        return (0) if (self.word_count == 0) else (self.character_count / self.word_count)
    
    def sentence_break_count(self):
        breakers = [".", "!", "?"]
        count = 0
        # TODO:
        # Remove ending parenthesis
        # Count only if the breaker ends the word
        for breaker in breakers:
            count += self.raw_data.count(breaker)

        return count

    def average_sentence_length(self):
        sentence_count = self.sentence_break_count()
        return (0) if (sentence_count == 0) else (self.character_count / sentence_count)

    def distribution_for_words_ending_by(self, ending):
        filtered_words = list(filter(lambda item: item.endswith(ending), self.sanitized_words))
        filtered_words.sort()
        return Counter(filtered_words)

    def extract_longest_word(self, count):
        filtered_words = list(set(self.sanitized_words))
        filtered_words.sort()
        filtered_words.sort(key=len, reverse=True)
        filtered_words = filtered_words[:count]
        return filtered_words

class Logger():

    _log_file = None

    def __init__(self, file_path):
        try:
            self._log_file = open(file_path, "w+")
        except IOError as error:
            print(error)

    def log(self, string):
        if self._log_file != None:
            self._log_file.write(string + "\n")
        else:
            print(string)

    def __del__(self):
        if self._log_file != None:
            self._log_file.close()
    
logger = Logger(OUTPUT_PATH)

def get_data_from_file(file_path):
    f = open(file_path, "r")
    data = f.read()
    f.close()
    return data

def task1():
    try:
        file_data = get_data_from_file(FILE_PATH)
    except IOError as error:
        print(error)
        return

    analysis = WordAnalysis(file_data)
    logger.log(TOTAL_WORD_COUNT.format(analysis.word_count))
    logger.log(TOTAL_CHARACTER_COUNT.format(analysis.character_count))
    logger.log(AVERAGE_WORD_LENGTH.format(analysis.average_word_length()))
    logger.log(AVERAGE_SENTENCE_LENGTH.format(analysis.average_sentence_length()))

    logger.log(LY_WORDS_DISTRIBUTION)
    distribution = analysis.distribution_for_words_ending_by("ly")
    for (word, count) in distribution.items():
        logger.log(WORD_DISTRIBUTION.format(word, count))

    logger.log(DESC_LONGEST_WORD)
    longest_words = analysis.extract_longest_word(10)
    logger.log(", ".join(longest_words))
        
task1()
