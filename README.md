# Summary

Noted is a python backend that keeps track of all the music played on your mac, across spotify, apple music, youtube, and other browser based streamers, using Apple's media controls. Using raw json, your data is 100% yours forever, stored on your computer, and never stored on the cloud. Noted also runs a MCP server that allows for data integration with llm's, allowing your music data to be used in countless ways, from visualization of trends to my favorite feature; Music recommendations that understand your tastes better than anyone, and aren't tainted by preserving spotify's bottom line. And of course under an MIT license, the source code is fully open source for modification and improvement.

# Features

Apart from plain data logging, Noted's MCP server allows your favorite llm to intelligently query your data instead loading 10's of thousands of tokens, giving you better results and saving you tokens.

# Supported apps

- Spotify
- Apple Music
- Web browsers(though they are not enabled by default to keep videos out of your data)
- Make a pr/ issue if you want something else added!

# Motive

As someone that listens to toooons of music, I found that spotify was feeding me the same 50 songs over and over and I know I'm not the only one. I dislike/ have little experience making frontends though, as I have an impossible time making them look good at all, and also wanted to experiment with creating my own mcp servers, after using many premade ones.

# Tech stack

- To get the actual now playing data from my mac, I used the nowplaying-cli, a great cli that exposes apple's music controls
- For better genre classification and indexing, I used an llm from openrouter using the ai.hackclub.com wrapper for free usage. Any llm provider would work here though.
- For the MCP server, I used FastMCP, as it seemed like a solid simple option for my very simple server.
- For the llm to connect to the server, I went with claude, as I have claude pro.

# Dependencies:

- Brew
- Git
- Python 3

# Install

- Please note that due to the core architecture of this project, it fundamentally only works on macs.
- Clone the repo, then double click the install.command file in finder
- create a .env, and add your ai.hackclub.com api key as HCAI=xxx
# AI statement

Claude was consulted for explaining errors, asking how to do things, and general educational assistance, though all of the code is hand written by me. This readme was properly formatted with claude too, though every single word is mine.
