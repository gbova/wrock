import tone_analyzer
import threading
import sys


# analyze
# Parameters: Text to be analyzed and the paragraph number it was in
# TODO: Store results of this method in a data structure for music creation
def analyze(text, paragraph):
    global MUTEX
    global CHARACTERS
    global ANALYZED_PARAGRAPHS

    tone = tone_analyzer.analyze_tone(text)
    if tone != False:
        print(tone)
        characters = tone_analyzer.extract_characters(CHARACTERS, text)
        metadata = {"paragraph" : paragraph,
                    "tone" : tone,
                    "characters": characters}
        MUTEX.acquire()
        ANALYZED_PARAGRAPHS.append(metadata)
        MUTEX.release()
    else:
        sys.stderr.write("Something went wrong!\n")



# open_book
# Parameters: The name of the file to open
# This method opens the file "characters.txt" and stores all character names
# and then opens the story file by the given name and returns the file pointer
def open_book(name):
    # There must be a file named "characters.txt" in the directory
    # If not, give the user an error message and exit
    try:
        file = open("characters.txt", "r")
        global CHARACTERS
        CHARACTERS = []
        for line in file:
            CHARACTERS.append(line.strip("\n"))
        file.close()
    except IOError:
        sys.stderr.write("Error: Characters.txt does not exist.\n")
        exit(1)

    # Open the text file with the story in it and return the pointer
    # If no story file exists, give the user an error message and exit
    try:
        book = open(name, "r")
        return book
    except IOError:
        sys.stderr.write("Error: File does not appear to exist.\n")
        exit(1)


# start
# This method starts the text analysis by opening the book and analyzing every line
# When the method returns, you know the story has been analyzed in full
def start():
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


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stderr.write("Too few arguments, please provide a text file.\n")
        exit(1)

    global ANALYZED_PARAGRAPHS
    ANALYZED_PARAGRAPHS = []
    global MUTEX
    MUTEX = threading.Semaphore()

    start()
