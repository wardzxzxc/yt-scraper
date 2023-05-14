import re

import requests as r
from bs4 import BeautifulSoup

from yt_scraper import constants


def get_generated_captions(video_id: str) -> str:
    yt_resp = r.get(
        constants.YOUTUBE_VIDEO_URL % video_id, headers=constants.REQUEST_HEADERS
    )
    yt_page_html = yt_resp.text
    regex = re.compile(constants.CAPTIONS_REGEX)
    url_transcript = regex.search(yt_page_html).group(1)
    decoded_url_transcript = url_transcript.encode("utf-8").decode("unicode-escape")
    captions_resp = r.get("https://www." + decoded_url_transcript)
    captions_html = BeautifulSoup(captions_resp.text, features="xml").get_text(
        separator=" "
    )

    captions = BeautifulSoup(captions_html, features="lxml").get_text()

    return captions
