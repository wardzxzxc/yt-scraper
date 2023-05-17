import re

import requests as r
from bs4 import BeautifulSoup

from yt_scraper import base, constants


class CaptionsScraper(base.Scraper):
    def __init__(self):
        super().__init__()
        self._base_url = constants.YOUTUBE_VIDEO_URL

    def get_items(self, video_id):
        resp = self._get(self._base_url % video_id)
        html = resp.text
        regex = re.compile(constants.CAPTIONS_REGEX)
        url_transcript = regex.search(html).group(1)
        decoded_url_transcript = url_transcript.encode("utf-8").decode("unicode-escape")
        captions_resp = r.get("https://www." + decoded_url_transcript)
        captions_html = BeautifulSoup(captions_resp.text, features="xml").get_text(
            separator=" "
        )

        captions = BeautifulSoup(captions_html, features="lxml").get_text()

        return captions

    def write_captions(self, file_path: str, video_id: str) -> None:
        captions = self.get_items(video_id)
        with open(file_path, "w+") as fh:
            fh.write(captions)
