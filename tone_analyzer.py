import requests
import json

WATSON = "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21"


# display_results
# Parameters: The data returned from IBM Watson's Tone Analyzer
# This method prints all tones of the text to standard output
def display_results(data):
    data = json.loads(str(data))
    if "error" in data:
        code = data["code"]
        error = data["error"]
        message = str(code) + ": " + error
        print(message)
        return
    # Print all tones associated with the analyzed text
    for tone in data["document_tone"]["tones"]:
        print(tone["tone_name"])


# extract_overall_tone
# Parameters: The data returned from IBM Watson's Tone Analyzer
# This method extracts the overall tone of the text analyzed by IBM Watson
def extract_tone(data):
    data = json.loads(data.encode("utf-8"))
    if "error" in data:
        return

    # Return the tone with the highest score. The default is Neutral
    overall_tone = "Neutral"
    overall_tone_score = -1
    for tone in data["document_tone"]["tones"]:
        current_tone = tone["tone_name"]
        current_score = tone["score"]
        if current_score > overall_tone_score:
            overall_tone = current_tone
            overall_tone_score = current_score
    return overall_tone


# analyze_tone
# Parameters: The text to be analyzed
# This method makes a call to IBM Watson's tone analyzer, with my credentials,
# and returns the results
def analyze_tone(text):
    # usr = "4fefa032-6a54-42c1-b941-052dc4b1f30c"
    # pwd = "vCiQRlTwiYSr"
    usr = "b7d346d9-6fa6-41c8-81fa-164455045633"
    pwd = "JSYk5elXU1Yn"
    headers = {"content-type": "text/plain"}
    data = text
    try:
        r = requests.post(WATSON, auth=(usr,pwd), headers=headers, data=data)
        tone = extract_tone(r.text)
        return tone
    except:
        return False


# extract_characters
# Parameters: A list of character names, a block of text
# Returns: The list of characters names that appear in the given text
def extract_characters(characters, text):
    character_list = []
    for character in characters:
        if character in text:
            character_list.append(character)
    return character_list
