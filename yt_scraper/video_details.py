from bs4 import BeautifulSoup

from yt_scraper import base, constants, schemas, utils


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
            "description": utils.regex_extract_value(
                '(?<="shortDescription":")(.*?)(?=")', string=html
            ),
            "statistics": self._get_statistics(html),
        }

        return schemas.VideoDetails(**kwargs)

    @staticmethod
    def _get_statistics(html: str):
        '(?<="views":{"simpleText":")(.*?)(?= views)'
        views_count = int(
            utils.regex_extract_value(
                '(?<="views":{"simpleText":")(.*?)(?= views)', string=html
            ).replace(",", "")
        )
        likes_count = int(
            utils.regex_extract_value(
                '(?<="label":")(.*?)(?= likes)', string=html
            ).replace(",", "")
        )
        return schemas.Statistics(views_count=views_count, likes_count=likes_count)
