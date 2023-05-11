from typing import List

import requests as r
from bs4 import BeautifulSoup

from yt_scraper import _constants as constants


def get_tags(video_id: str) -> List[str]:
    """
    Gi
    :param video_id:
    :return:
    """
    yt_resp = r.get(constants.YOUTUBE_URL % video_id, headers=constants.REQUEST_HEADERS)
    soup = BeautifulSoup(yt_resp.text, features="html.parser")
    return soup.find("meta", property="og:video:tag")
