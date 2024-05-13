import json
import subprocess


def download_youtube_media(options, media_content):
    # Importing here to avoid circular dependency
    from utils.utilities import get_output_template, logger

    # supported_audio_formats
    supported_audio_formats = ["m4a", "mp3", "wav", "ogg", "aac", "flac"]

    # Extracting From Options
    sub = options["sub"]
    url = options["url"]
    path = options["path"]
    format = options["format"]
    quality = options["quality"]
    embed_metadata = options["embed_metadata"]

    # FIXME:
    # Set Default Output Format To MKV
    # Will Be Used If There's No Format Defined
    # This is Hardcoded For Now, Should Be Changed
    # I Should Not Define Default Format Explicitly
    if format is None:
        format = "mp4"
        options["format"] = "mp4"

    # Creating Dictionary To Show To User
    media_info = {
        "id": media_content["id"],
        "format": media_content["ext"],
        "title": media_content["title"][:100],
        "thumbnail": media_content["thumbnail"],
        "resolution": media_content["resolution"],
        "website_name": media_content["extractor_key"],
        "options": {
            "sub": options["sub"],
            "url": options["url"],
            "path": options["path"],
            "format": options["format"],
            "quality": options["quality"],
            "embed_metadata": options["embed_metadata"],
        },
    }

    # Creating Path To Save Media & Generating Filename
    template_path, template_output = get_output_template(
        file_format=media_info["options"]["format"],
        website_name=media_info["website_name"],
        resolution=media_info["resolution"],
        title=media_info["title"],
        id=media_info["id"],
        template_path=path,
    )
    media_info["template_path"] = template_path
    media_info["template_output"] = template_output
    logger(json.dumps(media_info, indent=4), "success")

    if path or sub is not None:
        raise ValueError(
            logger(f"""
            Sub:{sub},
            Path:{path}
            is not supported by youtube_media downloader.
            """)
        )

    try:
        command = [
            "yt-dlp",
            f"-S res:{quality}",
            "--windows-filenames",
            # Create File Template & Output Format
            f"-P{media_info["template_path"]}",
            f"-o{media_info["template_output"]}",
            # Keep Download History
            "--download-archive",
            ".download_history.txt",
        ]

        # Define Output Format
        # Dont Do it For Audio Formats
        if format and format not in supported_audio_formats:
            command += ["--merge-output-format", format]

        # Embed Metadata
        # Dont Do it For Audio Formats
        if embed_metadata and format not in supported_audio_formats:
            command += ["--embed-metadata", "--embed-thumbnail"]

        if format in supported_audio_formats:
            command += [
                "-x",
                "--audio-format",
                format,
                "--embed-metadata",
                "--embed-thumbnail",
                "-v",
                "--convert-thumbnail",
                "jpg",
                "--ppa",
                # INFO:
                # Source: https://github.com/yt-dlp/yt-dlp/issues/429
                "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\"",
            ]

        # command.append()
        command.append(url)

        subprocess.run(command, check=True)
        logger(f"{media_content["title"]} has downloaded successfully", "success")

    except subprocess.CalledProcessError as e:
        logger(f"Error downloading youtube media: {e}", "warning")
