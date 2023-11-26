# 505 Semantic Search

Very much based off [Lilian Weng's Emoji Semantic Search](https://github.com/lilianweng/emoji-semantic-search/tree/main). You just need to set your `OPENAI_API_KEY`, and it should run locally! As for the messages, you can use [this](https://github.com/Tyrrrz/DiscordChatExporter) to export messages from Discord.

I mostly just wanted experience with JS and Python, and for any good source code, you should maybe go see other codebasees! If for some reason, you *would* like to try and get this working with your discord messages, do contact me, and I'll try my best to help out :)

## Build embeddings

```
OPENAI_API_KEY=[FILL HERE] python server/data/build.py
```

## Run server

```
OPENAI_API_KEY=[FILL HERE] python server/app.py
```

## Open client

```
open client/public/index.html
```