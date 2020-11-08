FILE_PATH = "book.txt"
OUTPUT_PATH = "summary.txt"

MISSING_LETTERS_OUTPUT = "It doesn't have all letters."
ALL_LETTERS_OUTPUT = "It has all letters."

ALL_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

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

def parse_data(raw_data):

    occurences = {}

    for letter in ALL_LETTERS:
        count = raw_data.upper().count(letter)
        if count != 0:
            occurences[letter] = count

    return occurences

def task2():
    try:
        file_data = get_data_from_file(FILE_PATH)
    except IOError as error:
        print(error)
        return

    occurences = parse_data(file_data)
    
    for value, count in occurences.items():
        logger.log("{} {}".format(value, count))
        
    if len(occurences) == len(ALL_LETTERS):
        logger.log("\n" + ALL_LETTERS_OUTPUT)
    else:
        logger.log("\n" + MISSING_LETTERS_OUTPUT)
        
task2()
