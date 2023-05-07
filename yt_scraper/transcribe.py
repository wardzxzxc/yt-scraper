import re

import _constants as constants
import requests as r
from bs4 import BeautifulSoup


def get_generated_captions(video_id: str, file_name: str):
    yt_resp = r.get(constants.YOUTUBE_URL + video_id, headers=constants.REQUEST_HEADERS)
    yt_page_html = yt_resp.text
    regex = re.compile(
        'playerCaptionsTracklistRenderer.*?(youtube.com/api/timedtext.*?)"'
    )
    url_transcript = regex.search(yt_page_html).group(1)
    decoded_url_transcript = url_transcript.encode("utf-8").decode("unicode-escape")
    captions_resp = r.get("https://www." + decoded_url_transcript)
    captions_html = BeautifulSoup(captions_resp.text, features="xml").get_text(
        separator=" "
    )

    captions = BeautifulSoup(captions_html, features="lxml").get_text()

    with open(file_name, "w+") as fh:
        fh.write(captions)


if __name__ == "__main__":
    get_generated_captions("K8r5pMxox7w", "transcript.txt")
