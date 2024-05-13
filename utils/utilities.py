import os
import re
import json
import click
import subprocess
from utils.download_generic_media import download_generic_media
from utils.download_youtube_media import download_youtube_media
from utils.download_facebook_media import download_facebook_media


def fetch_media_content(options):
    command = [
        "yt-dlp",
        "--dump-single-json",
        "--skip-download",
        options["url"],
    ]

    try:
        output = subprocess.check_output(command)
        output_str = output.decode("utf-8")
        json_data = json.loads(output_str)

        # extracted_data = {
        #     "thumbnail": json_data["thumbnail"],
        #     "subtitles": json_data["subtitles"],
        #     "title": json_data["title"],
        #     "playlist": json_data["playlist"],
        #     # "video_ext": json_data["video_ext"],
        #     # "audio_ext": json_data["audio_ext"],
        #     "resolution": json_data["resolution"],
        #     # "formats": json_data["formats"],
        # }
        return json_data

    except subprocess.CalledProcessError as e:
        # Handle errors if the command execution fails
        print("Error executing command:", e)
        return None

    except json.JSONDecodeError as e:
        # Handle errors if the JSON parsing fails
        print("Error parsing JSON:", e)
        return None

    # click.echo(json.dumps(media_content, indent=4))


def download_media(options, media_content):
    url = options["url"]

    url_patterns = {
        "youtu.be": download_youtube_media,
        "fb.watch": download_facebook_media,
        "youtube.com": download_youtube_media,
        "facebook.com": download_facebook_media,
    }

    for pattern, download_function in url_patterns.items():
        if pattern in url:
            download_function(options, media_content)
            break
    else:
        download_generic_media(options, media_content)


def get_output_template(
    id=None,
    title=None,
    resolution=None,
    file_format=None,
    website_name=None,
    template_path=None,
):
    # Make it smaller case to match
    # .download_history.txt's extractor_key name
    if website_name:
        website_name = website_name.lower()

    if title:
        title = title.replace(" ", "_")
        title = re.sub(r"\[([^][]+)\]", "", title)
        title = title.replace("/", "")

    if template_path is None:
        template_path = os.getcwd()

    if not os.path.exists(template_path):
        raise FileNotFoundError("Path does not exist.")

    # Count the number of existing files with the given format
    file_count = 0
    if file_format:
        for filename in os.listdir(template_path):
            if filename.endswith("." + file_format):
                file_count += 1

    # Generate yt-dlp output template
    if file_count == 0:
        template_output = f"[0] [{website_name}] [{title}] [{id}].{file_format}"
    else:
        template_output = (
            f"[{file_count}] [{website_name}] [{title}] [{id}].{file_format}"
        )

    return template_path, template_output


def logger(message, message_type="info", **kwargs):
    formatted_message = message.format(**kwargs) if kwargs else message

    if message_type == "success":
        click.secho(formatted_message, fg="green")
    elif message_type == "warning":
        click.secho(formatted_message, fg="yellow")
    elif message_type == "error":
        click.secho(formatted_message, fg="red", bold=True)
    else:
        click.echo(formatted_message)


# Define the function to update download history
def update_download_history(path, format):
    pattern = r"\[(.*?)\]"
    if path is None:
        path = os.getcwd()

    if path is None or not os.path.isdir(path):
        raise LookupError(logger(f"Path: {path} Doesn't Exist!"), "error")

    files = [f for f in os.listdir(path) if f.endswith(format)]
    files.sort()

    history_data = []
    expected_count = 0

    for file_name in files:
        matches = re.findall(pattern, file_name)
        if matches:
            file_count = int(matches[0])
            website_name = matches[1]
            title = matches[2]
            video_id = matches[3]

            # Update .download_history.txt file
            with open(os.path.join(path, ".download_history.txt"), "w") as history_file:
                history_file.write(f"{website_name} {video_id}\n")

            # Update file names if necessary
            if file_count == expected_count:
                logger(
                    f"Skipping: [{file_count}] is alright! no need to rename file!",
                    "success",
                )

            else:
                new_file_name = f"[{expected_count}] [{website_name}] [{title}] [{video_id}].{format}"
                os.rename(
                    os.path.join(path, file_name), os.path.join(path, new_file_name)
                )
                logger(f"Renamed {file_name}", "warning")
                logger(f"To {new_file_name}", "success")

            expected_count += 1
            history_data.append(f"{website_name} {video_id}")

        else:
            raise LookupError(logger("no match found in path {path}", "error"))

    with open(os.path.join(path, ".download_history.txt"), "w") as history_file:
        for data in history_data:
            history_file.write(data + "\n")
