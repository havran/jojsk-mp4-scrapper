# joj.sk shows episodes video links crawler
Fetches all links to videos for episodes from archive to JSON.
# usage
```
python crawler.py
```
result:
```
[
  {
    "season": "1. séria",
    "episodes": [
      {
        "episode": "Inkognito E1",
        "videoLinks": {
          "360p": "https://nn.geo.joj.sk/storage/media-new/vod/2018/01/09/04f147e4-7a96-43a2-a45c-23397d5d0c32-360p.mp4",
          "540p": "https://nn.geo.joj.sk/storage/media-new/vod/2018/01/09/04f147e4-7a96-43a2-a45c-23397d5d0c32-540p.mp4",
          "720p": "https://nn.geo.joj.sk/storage/media-new/vod/2018/01/09/04f147e4-7a96-43a2-a45c-23397d5d0c32-720p.mp4"
        }
      },
      ...
    ]
  },
...
]
```

# requirements
```
beautifulsoup4==4.6.0
certifi==2018.8.24
requests==2.18.4
more-itertools==4.3.0
```

# disclaimer
Use at you own risk and read joj.sk TOS.
