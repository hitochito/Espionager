import click
from pytube import Playlist
from utils.utilities import (
    download_media,
    fetch_media_content,
    update_download_history,
)


# CLI command
@click.command()
@click.argument("url")
@click.option(
    "-p",
    "--path",
    help="Directory path to save this file (default: current path)",
    default=None,
)
@click.option(
    "-o",
    "--format",
    help="Output format / file extension(e.g., mp4, mp3, wav, m4a, mkv)",
    default=None,
)
@click.option(
    "-q",
    "--quality",
    help="Video quality (e.g., 1080, 720, 480, 2160)",
    default="1080",
)
@click.option(
    "-s",
    "--sub",
    help="Subtitle language to embed in media (e.g., en, bn)",
    default=None,
)
@click.option(
    "-em",
    "--embed-metadata",
    help="Allow metadata embedding (default: True)",
    default=True,
)
def esp(url, format, quality, sub, path, embed_metadata):
    if url == "update-download-history":
        update_download_history(path, format)
    else:
        url_list = url.split(",")
        for single_url in url_list:
            single_url = single_url.strip()
            options = {
                "sub": sub,
                "path": path,
                "format": format,
                "quality": quality,
                "embed_metadata": embed_metadata,
            }

            # INFO:
            # Detect If Its a YouTube Playlist
            # If so, Extract Them & Run a Loop To Download Them
            if "?list=" in single_url:
                playlist = Playlist(single_url)
                for single_youtube_url in playlist:
                    options["url"] = single_youtube_url
                    media_content = fetch_media_content(options)
                    download_media(options, media_content)

            else:
                options["url"] = single_url
                media_content = fetch_media_content(options)
                download_media(options, media_content)


if __name__ == "__main__":
    esp()
