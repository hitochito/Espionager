# Commands (For Building) (In Windows)

- pyinstaller --onefile --name esp esp.py

# Basic Idea

I want to download any video from any source that can be possible to be downloaded by yt-dlp.

# WHAT IS ESPIONAGER?

This is a personal project I've been working on to download and manage media.
ESPIONAGER is a Python-based script designed for covert media acquisition.
It allows users to download media content from various sources, including YouTube and other video sites.
The script supports downloading both video and audio formats, enabling users to save content as MP3 or video files.
Additionally, ESPIONAGER offers the capability to tag downloaded music files and specify the resolution format for downloads.

# IDEAS

publish this as a npm package? I guess that would be kinda cool!

# How It Should Be?

I want to type 'esp' and all these values:

## sub

It will add subtitle to the video, defaults to english. Can be changed using `sub:{language}`

## mp4/mp3/m4a/mkv or any other supported video format

If no format is specified then it will be the default format yt-dlp chooses.
After downloading the video, it will convert the video to the specified format.

## quality (1080p, 720p, 480p, 2160p)

manually writing video quality is also supported.
The quality defaults to 1080p if available and provided by the user or the next best available quality.

## allow_metadata (can be `true` or `false`)

Defaults to `true` meaning it embeds the metadata after downloading.
If its an video file then it embeds the metadata from the source.
If its an audio file then it tries to find metadata from shazam, spotify, or other music sources and embeds those metadata
