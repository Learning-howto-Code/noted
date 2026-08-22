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
history_file =  Path(__file__).parent / "history.json"
load_dotenv()
model = 'z-ai/glm-5.2:free'
nowplaying = "/opt/homebrew/bin/nowplaying-cli"

with open ("allowlist.txt", "r") as j:
    allowlist = j.read()
with open ("allowlist.txt", "r") as j:
    allowlist = set(j.read().split())
with open ("banlist.txt", "r") as j:
    banlist = set(j.read().split())

def get_song():
    global nowplaying
    info = subprocess.run([nowplaying, "get-raw", "--json"], capture_output=True, text=True)
    info= info.stdout.strip()
    song_dict= json.loads(info)
    song_dict.pop("kMRMediaRemoteNowPlayingInfoArtworkData", None)
    old_keys = {
        "kMRMediaRemoteNowPlayingInfoArtist": "artist",
        "kMRMediaRemoteNowPlayingInfoTitle": "title",
        "kMRMediaRemoteNowPlayingInfoDuration": "duration",
        "kMRMediaRemoteNowPlayingInfoAlbum": "album",
        "kMRMediaRemoteNowPlayingInfoGenre": "genre",
        "kMRMediaRemoteNowPlayingInfoElapsedTime": "elapsed",
        "kMRMediaRemoteNowPlayingInfoTrackNumber": "track_number",
        "kMRMediaRemoteNowPlayingInfoClientBundleIdentifier": "application"
    }
    for old, new in old_keys.items():
        if old in song_dict:
            song_dict[new] = song_dict.pop(old)
    return song_dict

song_dict = get_song()
def get_song_info(song_dict):
    global HCAI
    HCAI = os.getenv("HCAI")
    # print("loaded api key")
    client = OpenRouter(
        api_key=HCAI,
        server_url="https://ai.hackclub.com/proxy/v1",
    )
    # print("sent response")
    response = client.chat.send(
        model=model,
        messages=[
            {"role": "user", "content": f"You describe the vibe of a song in 8-12 words. Output a comma-separated list of descriptors covering genre, mood, texture, and setting. Do not write a full sentence. Go beyond one-word labels like \"pop\" or \"rock\" — be specific and evocative. If you don't know the song, infer from the artist's typical style. Output only the descriptors. No preamble, no quotes, no trailing period. If you don't know the song, DO NOT GUESS UNDER ANY CIRCUMSTANCES, instead say genre unknown. Sometimes, ads being played also get picked up, if the title is pbviously an ad, like Doordash etc always say 'Advertisement, IGNORE ENTRY'. It is better to default to saying it's an ad than letting ads get through.   The song you are describing is {song_dict['title']} by {song_dict['artist']}. The given genre is "},
        ],
        max_tokens=2000,
        temperature=0,
        stream=False,
    )
    # print(f"message was You describe the vibe of a song in 8-12 words. Output a comma-separated list of descriptors covering genre, mood, texture, and setting. Do not write a full sentence. Go beyond one-word labels like \"pop\" or \"rock\" — be specific and evocative. If you don't know the song, infer from the artist's typical style. Output only the descriptors. No preamble, no quotes, no trailing period.  The song you are describing is {song_dict['title']} by {song_dict['artist']}.")
    # print("sent response")
    response = response.choices[0].message.content
    # print("got response")
    # print(response)
    return response
def log_song(song_dict, response, elapsed_time):
    global current
    with open(history_file, "r")as f:
        try:
            old = json.load(f)
        except json.JSONDecodeError:
            old = []
    if (song_dict.get("duration")) == 'null':
        duration = 0
    else:
        duration= float(song_dict.get("duration", 0))
    m,s = divmod(int(duration), 60)
    duration = f"{m}:{s:02d}"
    current={
        "Artist": song_dict["artist"],
        "Title": song_dict["title"],
        "Duration": song_dict["duration"],
        "Genre" : song_dict.get("genre"),
        "Description": response,
        "Date": time.strftime("%Y-%m-%d %H:%M", time.localtime()),
        "Played song for(seconds)": elapsed_time,
        "Application": song_dict["application"]
    }


    old.append(current)
    with open(history_file, "w") as i:
        json.dump(old, i, indent=4)
    # print(info)
def check_app_type(song_dict):
    global allowlist, banlist
    app= song_dict.get("application")

    if app not in allowlist and app not in banlist:
        application = song_dict["application"]
        HCAI = os.getenv("HCAI")
        # print("loaded api key")
        client = OpenRouter(
            api_key=HCAI,
            server_url="https://ai.hackclub.com/proxy/v1",
        )
        # print("sent response")
        response = client.chat.send(
            model=model,
            messages=[
                {"role": "user", "content": f"I need to know if the given url is for streaming music, or if it is for streaming any other type of media like video, podcasts, or audiobooks. If it is for streaming music, respond with 'music'. If it is for streaming any other type of media, respond with 'not music'. The url you are checking is {application}. Do not respond with anything else. If it is a niche website or you don't know ALWAYS SAY NOT MUSIC. NEVER GUESS!!"},
            ],
            max_tokens=2000,
            stream=False,
        )
        response = response.choices[0].message.content.strip().lower()
        # print(response)
        if response == "music":
            allowlist.add(song_dict["application"])
        else:
            banlist.add(app)
        with open("allowlist.txt", "w") as f:
            f.write("\n".join(allowlist))
        with open("banlist.txt", "w") as f:
            f.write("\n".join(banlist))
        # print("updated allow/ban list")
        # print("\n".join(banlist))
        # print("\n".join(allowlist))
        return response

current_song=None
old_song= None
elapsed_time = 0
old_song_dict = song_dict
while True:
    song_dict = get_song() # gets song info
    if not song_dict.get("application") or not song_dict.get("title"):
        # print("nothing playing") # ensures that it doesn't crash with empty logs
        time.sleep(5)
        continue

    response = check_app_type(song_dict)
    if song_dict["application"] in allowlist: # only runs if app is aproved
        # print(f"got song, song is {song_dict['title']}")
        current_song = song_dict["title"]

        if current_song != old_song or current_song == None:  #When the current song changes, we want to log
            response = get_song_info(song_dict)
            # print(f"got response, response is {response}")
            old_song_dict["Played song for(seconds)"] = elapsed_time
            log_song(old_song_dict, response, elapsed_time)
            old_song_dict = song_dict
            # print("logged song")
            elapsed_time = 0

        elif current_song == old_song:
            # print("no change, not logging")
            # print(f"current song: {current_song}, old song: {old_song}")
            pass
        old_song = current_song
        if elapsed_time < 500:
            elapsed_time += 5
        else :
            elapsed_time == 500
        time.sleep(5)
