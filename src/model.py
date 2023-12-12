from datetime import datetime
from typing import Optional


class Video:
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title


class Post:

    def __init__(self, published: datetime, title: str, link: str, excerpt: str):
        self.published = published
        self.title = title
        self.link = link
        self.excerpt = excerpt

    def __repr__(self) -> str:
        return f'Post(title={self.title}, link={self.link})'


class Conference:
    def __init__(self, name: str, url: Optional[str]):
        self.name = name
        self.url = url

    def __repr__(self) -> str:
        return f'Conference(name={self.name})'


class Talk:
    def __init__(self, title: str, link: Optional[str], summary: Optional[str], start_date: datetime, conference: Conference):
        self.title = title
        self.link = link
        self.summary = summary
        self.start_date = start_date
        self.conference = conference

    def __repr__(self) -> str:
        return f'Talk(title={self.title}, link={self.link}), description={self.summary}, conference={self.conference.name})'
