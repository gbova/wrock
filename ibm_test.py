import tone_analyzer
import threading
import sys


# analyze
# Parameters: Text to be analyzed and the paragraph number it was in
# Returns: Paragraph number, paragraph tone, list of appearing characters
# TODO: Store results of this method in a data structure for music creation
def analyze(text, paragraph):
    global IO_MUTEX
    global CHARACTERS
    results = tone_analyzer.analyze_tone(text)
    if results != False:
        message = str(paragraph)
        tone = tone_analyzer.extract_tone(results)
        message += " " + tone
        characters = tone_analyzer.extract_characters(CHARACTERS, text)
        message += " " + str(characters)

        IO_MUTEX.acquire()
        print(message)
        IO_MUTEX.release()
    else:
        sys.stderr.write("Something went wrong!\n")
    return


# open_book
# Parameters: The name of the file to open
# This method opens the file "characters.txt" and stores all character names
# and then opens the story file by the given name and returns the file pointer
def open_book(name):
    try:
        file = open("characters.txt", "r")
        global CHARACTERS
        CHARACTERS = []
        for line in file:
            CHARACTERS.append(line.strip("\n"))
        file.close()
    except IOError:
        sys.stderr.write("Error: File does not appear to exist.\n")
        exit(1)

    try:
        book = open(name, "r")
        return book
    except IOError:
        sys.stderr.write("Error: File does not appear to exist.\n")
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stderr.write("Too few arguments, please provide a text file.\n")
        exit(1)

    THREADS = threading.Semaphore(10)
    global IO_MUTEX          # TODO: Change this mutex; will be used to update music data structure
    IO_MUTEX = threading.Semaphore()

    title = sys.argv[1]
    book = open_book(title)
    for lineNum, line in enumerate(book, start=1):
        THREADS.acquire()
        thread = threading.Thread(target=analyze, args=(line, lineNum))
        thread.start()
        THREADS.release()
    book.close()
