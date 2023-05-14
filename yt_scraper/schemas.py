import dataclasses
from typing import List


@dataclasses.dataclass
class Statistics:
    views_count: int
    likes_count: int


@dataclasses.dataclass
class VideoDetails:
    tags: List[str]
    description: str
    title: str
    statistics: Statistics
