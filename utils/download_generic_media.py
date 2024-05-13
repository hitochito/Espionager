import json
import subprocess


def download_generic_media(options, media_content):
    # Importing here to avoid circular dependency
    from utils.utilities import get_output_template, logger

    # Extracting From Options
    sub = options["sub"]
    url = options["url"]
    path = options["path"]
    format = options["format"]
    quality = options["quality"]
    embed_metadata = options["embed_metadata"]

    # Creating Dictionary To Show To User
    print_media_info = {
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
        website_name=print_media_info["website_name"],
        resolution=print_media_info["resolution"],
        file_format=print_media_info["format"],
        title=print_media_info["title"],
        id=print_media_info["id"],
        template_path=path,
    )
    print_media_info["template_path"] = template_path
    print_media_info["template_output"] = template_output
    logger(json.dumps(print_media_info, indent=4), "success")

    if path or sub or format is not None:
        raise ValueError(
            logger(f"""
            Sub:{sub},
            Path:{path},
            Format:{format}
            is not supported by generic_media downloader.
            """)
        )

    try:
        command = [
            "yt-dlp",
            f"-S res:{quality}",
            "--windows-filenames",
            # Create File Template & Output Format
            f"-P{print_media_info["template_path"]}",
            f"-o{print_media_info["template_output"]}",
            # Keep Download History
            "--download-archive",
            ".download_history.txt",
        ]

        # Embed Metadata
        if embed_metadata:
            command.append("--embed-metadata")
            command.append("--embed-thumbnail")

        # command.append()
        command.append(url)

        subprocess.run(command, check=True)
        logger(f"{media_content["title"]} has downloaded successfully", "success")

    except subprocess.CalledProcessError as e:
        logger(f"Error downloading generic media: {e}", "warning")
