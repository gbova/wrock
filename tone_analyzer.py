# tone_analyzer.py
# contains functions to analyze the tone of a paragraph and extract
#   a list of appearing characters or objects

import requests
import json

WATSON = "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version\
=2017-09-21"

def extract_tone(data):
    """extract_tone:
    Parameters: The data returned from IBM Watson's Tone Analyzer
    This method extracts the overall tone of the text analyzed by IBM Watson"""
    data = json.loads(data.encode("utf-8"))

    # Return None if there is an error in the data
    if "error" in data:
        return None

    # Return the tone with the highest score
    overall_tone = "Neutral"    # default to Neutral if no other tone found
    overall_tone_score = -1
    for tone in data["document_tone"]["tones"]:
        # Iterate over all tones in the data set, updating overall_tone and
        # overall_tone_score at every step, to find tone with highest score
        current_tone = tone["tone_name"]
        current_score = tone["score"]
        if current_score > overall_tone_score:
            overall_tone = current_tone
            overall_tone_score = current_score
    return overall_tone


def analyze_tone(text):
    """analyze_tone:
    Parameters: The text to be analyzed
    This method makes a call to IBM Watson's tone analyzer, with my credentials,
    and returns the results"""

    usr = "b7d346d9-6fa6-41c8-81fa-164455045633"
    pwd = "JSYk5elXU1Yn"
    headers = {"content-type": "text/plain"}
    data = text
    try:
        # make request
        r = requests.post(WATSON, auth=(usr,pwd), headers=headers, data=data)
        tone = extract_tone(r.text)
        return tone
    except:
        return False


def extract_characters(characters, text):
    """extract_characters:
    Parameters: A list of character names, a block of text
    Returns: The list of characters names that appear in the given text"""
    character_list = []
    for character in characters:
        if character in text:
            character_list.append(character)
    return character_list
