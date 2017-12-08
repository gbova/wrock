# wrock.py
# Main module that runs the program. Coordinates the tone analyzer and
#   music generator to play a soundtrack for a given passage based on its
#   changing sentimental tone and occuring characters/objects

import musicGenerator
import tone_analyzer
import threading
import sys

def analyze(text, paragraph):
    """ analyze:
    Parameters: Text to be analyzed and the paragraph number it was in.
    Stores results of this method in a data structure for music creation """
    global MUTEX
    global CHARACTERS
    global ANALYZED_PARAGRAPHS

    # analyze tone for this paragraph
    tone = tone_analyzer.analyze_tone(text)
    if tone != False:
        # extract characters that appear in paragraph, and add data to table
        characters = tone_analyzer.extract_characters(CHARACTERS, text)
        metadata = {"tone" : tone,
                   "characters" : characters}
        MUTEX.acquire()
        ANALYZED_PARAGRAPHS[paragraph] = metadata
        MUTEX.release()
    else:
        sys.stderr.write("Something went wrong!\n")


def open_book(name):
    """ open_book:
    Parameters: The name of the file to open
    This method opens the file "characters.txt" and stores all character names
    and then opens the story file by the given name and returns its file pointer
    """
    # There must be a file named "characters.txt" in the directory
    # If not, give the user an error message and exit
    try:
        file = open("characters.txt", "r")
        global CHARACTERS
        CHARACTERS = []
        for line in file:
            CHARACTERS.append(line.partition(":")[0])
        file.close()
    except IOError:
        sys.stderr.write("Error: characters.txt does not exist.\n")
        exit(1)

    # There must be a file named "tones.txt" in the directory
    # If not, give the user an error message and exit
    try:
        file = open("tones.txt", "r")
        file.close()
    except IOError:
        sys.stderr.write("Error: tones.txt does not exist.\n")
        exit(1)

    # Open the text file with the story in it and return the pointer
    # If no story file exists, give the user an error message and exit
    try:
        book = open(name, "r")
        return book
    except IOError:
        sys.stderr.write("Error: File does not appear to exist.\n")
        exit(1)


def start():
    """Starts the text analysis by opening the book and analyzing every line.
    When the method returns, the story has been analyzed in full"""
    title = sys.argv[1]
    book = open_book(title)
    threads = []

    # Iterate through every line and create a thread to analyze its tone
    for lineNum, line in enumerate(book, start=1):
        t = threading.Thread(target=analyze, args=(line, lineNum))
        t.start()
        threads.append(t)
    book.close()

    # Join every thread; they stop running when all the text is analyzed
    for t in threads:
        t.join()

    # Compile data for music generation
    music_gen = musicGenerator.musicGenerator(
            ANALYZED_PARAGRAPHS,
            100,
            "characters.txt",
            "tones.txt")

    music_gen.start()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stderr.write("Too few arguments, please provide a text file.\n")
        exit(1)

    global ANALYZED_PARAGRAPHS
    ANALYZED_PARAGRAPHS = {}
    global MUTEX
    MUTEX = threading.Semaphore()

    start()
