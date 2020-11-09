import string
from collections import Counter

"""
The word analysis is performed in the WordAnalysis class as per the assumptions below: 

# General Informations
- The name of the file to be analysed is provided in the "FILE_PATH" global variable. Default value is "task1-content.txt"

# Definitions
- Is considered a word any chunk of one or more characters.
- A word is separated from another word by either a space or a line return.
    > Example: "taxpayer-funded", "U.S.-Mexico-Canada" and "401(k)s" are considered a word.

- Is considered a sentence any group of one or more words that ends with one of the following punctuation signs: (. / ! / ?)
    > Example 1: "(Applause.)" and "USA!" are considered a sentence.
    > Example 2: "(applause)" is NOT considered a sentence, but is still part of larger sentence.

# Analysis Rules
- The word length is based on the count of characters that compose the word excepted trailing and leading non-alphanumerical characters.
    > Example 1: All characters are counted in "taxpayer-funded" and "U.S.-Mexico-Canada".
    > Example 2: The parenthesis and the final punctuation are NOT counted in "(Applause.)"

- The average sentence length is based on the total number of ponctuation signs (. / ! / ?) that *ends* a word.

- The longest words are determined as per the definitions above, and are sorted alphabetically when of equal length.

- Character casing is homogenised before processing, when relevant.
"""

FILE_PATH = "task1-content.txt"
OUTPUT_PATH = "summary.txt"

TOTAL_WORD_COUNT = "Total word count: {}"
TOTAL_CHARACTER_COUNT = "Total character count: {}"
AVERAGE_WORD_LENGTH = "The average word length: {:.2f}"
AVERAGE_SENTENCE_LENGTH = "The average sentence length: {:.2f}"
LY_WORDS_DISTRIBUTION = "\nA word distribution of all words ending in \"ly\":"
WORD_DISTRIBUTION = "{}: {}"
DESC_LONGEST_WORD = "\nA list of top 10 longest words in descending order:"

class WordAnalysis():
    raw_data = ""
    words = []
    sanitized_words = []
    word_count = 0
    character_count = 0

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
            self.sanitized_words.append(s_word.title())

    def average_word_length(self):
        sanitized_words_total_length = 0

        for word in self.sanitized_words:
            sanitized_words_total_length += len(word)

        return (0) if (self.word_count == 0) else (sanitized_words_total_length / self.word_count)
    
    def sentence_break_count(self):
        breakers = [".", "!", "?", ".)"]
        count = 0

        for word in self.words:
            for breaker in breakers:
                if word.endswith(breaker):
                    count += 1
                    break

        return count

    def average_sentence_length(self):
        sentence_count = self.sentence_break_count()
        return (0) if (sentence_count == 0) else (self.word_count / sentence_count)

    def distribution_for_words_ending_by(self, ending):
        filtered_words = list(filter(lambda item: item.endswith(ending), self.sanitized_words))
        filtered_words.sort()
        return Counter(filtered_words)

    def extract_longest_words(self, count):
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
    longest_words = analysis.extract_longest_words(10)
    logger.log(", ".join(longest_words))
        
task1()
