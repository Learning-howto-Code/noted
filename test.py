"""
Plan:
Get song title and artist, query spotify and apple music
Parse output, input into json
loop every 5 seconds, only log on change
"""
from math import inf
import os
import subprocess
from dotenv import load_dotenv # type: ignore
import json
import time
from openrouter import OpenRouter
from pathlib import Path

model = 'poolside/laguna-s-2.1:free'
load_dotenv()


song_dict = {
        "Artist": "Daft Punk",
        "Title": "Give Life Back to Music",
        "Duration": 274.4030612244898,
        "Genre": "Pop",
        "Description": "Disco-funk, euphoric, celebratory, live-band, analog, punchy, glossy, shimmering, dancefloor, retro-futuristic, triumphant",
        "Date": "2026-08-01 17:15",
        "Played song for(seconds)": 0.024352626,
        "Application": "com.apple.Music"
    }

def get_song_info(song_dict):
    global HCAI
    HCAI = os.getenv("HCAI")
    print("loaded api key")
    client = OpenRouter(
        api_key=HCAI,
        server_url="https://ai.hackclub.com/proxy/v1",
    )
    print("sent response")
    response = client.chat.send(
        model=model,
        messages=[
            {"role": "user", "content": f"You describe the vibe of a song in 8-12 words. Output a comma-separated list of descriptors covering genre, mood, texture, and setting. Do not write a full sentence. Go beyond one-word labels like \"pop\" or \"rock\" — be specific and evocative. If you don't know the song, infer from the artist's typical style. Output only the descriptors. No preamble, no quotes, no trailing period. If you don't know the song, DO NOT GUESS UNDER ANY CIRCUMSTANCES, instead say genre unknown  The song you are describing is {song_dict['Title']} by {song_dict['Artist']}. The given genre is "},
        ],
        stream=False,
    )
    print(f"message was You describe the vibe of a song in 8-12 words. Output a comma-separated list of descriptors covering genre, mood, texture, and setting. Do not write a full sentence. Go beyond one-word labels like \"pop\" or \"rock\" — be specific and evocative. If you don't know the song, infer from the artist's typical style. Output only the descriptors. No preamble, no quotes, no trailing period.  The song you are describing is {song_dict['Title']} by {song_dict['Artist']}.")
    print("sent response")
    response = response.choices[0].message.content
    print("got response")
    print(response)
    return response
response = get_song_info(song_dict)