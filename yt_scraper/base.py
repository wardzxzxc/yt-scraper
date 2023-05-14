import abc
import logging
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter, Retry

from yt_scraper import constants

_logger = logging.getLogger(__name__)


class Scraper(abc.ABC):
    """
    Abstract base class for scraper
    """

    def __init__(self, *, retries: int = 3, proxies: Optional[Dict[str, Any]] = None):
        self._retries = Retry(
            total=retries, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504]
        )
        self._proxies = proxies
        self._session = requests.Session()
        self._session.mount("https://", HTTPAdapter(max_retries=self._retries))

    @abc.abstractmethod
    def get_items(self):
        """
        Abstract method needed to get the respective resources
        """
        pass

    def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        if headers is None:
            headers = constants.REQUEST_HEADERS

        req = requests.Request(
            method=method, headers=headers, params=params, data=data, url=url
        )
        prepped_req = req.prepare()
        try:
            resp = self._session.send(
                prepped_req, proxies=self._proxies if self._proxies else {}
            )
        except requests.HTTPError as exc:
            _logger.error(f"HTTP error encountered: {exc}")

        return resp

    def _get(self, *args, **kwargs):
        return self._request("GET", *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request("POST", *args, **kwargs)
