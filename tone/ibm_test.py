import tone_analyzer

if __name__ == "__main__":
    with open("harrypotter1.txt", "r") as book:
        for paragraph in book:
            results = tone_analyzer.analyze_tone(paragraph)
            if results != False:
                print(tone_analyzer.extract_tone(results))
            else:
                print("Something went wrong!")
