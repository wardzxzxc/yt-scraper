import re

from bs4 import BeautifulSoup

from yt_scraper import base, constants, schemas


class VideoDetailsScraper(base.Scraper):
    def __init__(self):
        super().__init__()
        self._base_url = constants.YOUTUBE_VIDEO_URL

    def get_items(self, video_id: str):
        resp = self._get(self._base_url % video_id)
        html = resp.text
        soup = BeautifulSoup(html, features="html.parser")
        kwargs = {
            "tags": [
                i["content"] for i in soup.find_all("meta", property="og:video:tag")
            ],
            "title": soup.find("meta", property="og:title")["content"],
            "description": re.compile('(?<="shortDescription":")(.*?)(?=")')
            .search(html)
            .group(1),
            "statistics": self._get_statistics(html),
        }

        return schemas.VideoDetails(**kwargs)

    @staticmethod
    def _get_statistics(self, html: str):
        views_count = int(
            re.compile('(?<="views":{"simpleText":")(.*?)(?= views)')
            .search(html)
            .group(1)
            .replace(",", "")
        )
        likes_count = int(
            re.compile('(?<="label":")(.*?)(?= likes)')
            .search(html)
            .group(1)
            .replace(",", "")
        )
        return schemas.Statistics(views_count=views_count, likes_count=likes_count)
