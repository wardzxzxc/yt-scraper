import re

from bs4 import BeautifulSoup

from yt_scraper import base, constants


class VideoDetailsScraper(base.Scraper):
    def __init__(self):
        super().__init__()
        self._base_url = constants.YOUTUBE_VIDEO_URL

    def get_items(self, video_id: str):
        resp = self._get(self._base_url % video_id)
        html = resp.text
        soup = BeautifulSoup(html, features="html.parser")
        tags = [i["content"] for i in soup.find_all("meta", property="og:video:tag")]
        title = soup.find("meta", property="og:title")["content"]
        description = (
            re.compile('(?<="shortDescription":")(.*?)(?=")').search(html).group(1)
        )
        return {"tags": tags, "title": title, "description": description}
