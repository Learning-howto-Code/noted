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

model = 'z-ai/glm-5.2:free'
load_dotenv()


song_dict = {
        "Artist": "Billie Eilish",
        "Title": "BIRDS OF A FEATHER",
        "Duration": 210.373,
        "Genre": "null",
        "Description": "null",
        "Date": "2026-08-20 17:46",
        "Played song for(seconds)": 200,
        "Application": "com.spotify.client"
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
            {"role": "user", "content": f"You describe the vibe of a song in 8-12 words. Output a comma-separated list of descriptors covering genre, mood, texture, and setting. Do not write a full sentence. Go beyond one-word labels like \"pop\" or \"rock\" — be specific and evocative. If you don't know the song, infer from the artist's typical style. Output only the descriptors. No preamble, no quotes, no trailing period. If you don't know the song, DO NOT GUESS UNDER ANY CIRCUMSTANCES, instead say genre unknown. Sometimes, ads being played also get picked up, if the title is pbviously an ad, like Doordash etc always say 'Advertisement, IGNORE ENTRY'. It is better to default to saying it's an ad than letting ads get through.   The song you are describing is {song_dict['Title']} by {song_dict['Artist']}. The given genre is "},
        ],
        max_tokens=2000,
        stream=False,
    )
    print(f"message was You describe the vibe of a song in 8-12 words. Output a comma-separated list of descriptors covering genre, mood, texture, and setting. Do not write a full sentence. Go beyond one-word labels like \"pop\" or \"rock\" — be specific and evocative. If you don't know the song, infer from the artist's typical style. Output only the descriptors. No preamble, no quotes, no trailing period.  The song you are describing is {song_dict['Title']} by {song_dict['Artist']}.")
    print("sent response")
    response = response.choices[0].message.content
    print("got response")
    print(response)
    return response
response = get_song_info(song_dict)