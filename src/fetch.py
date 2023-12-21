from datetime import datetime, date
from os import getenv
from typing import Optional, Mapping
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from requests import get
from yaml import safe_load

from model import Post, Talk, Video, Conference

blog_repo_path = 'nfrankel%2Fnfrankel.gitlab.io'


def bio() -> str:
    url = f'https://gitlab.com/api/v4/projects/{blog_repo_path}/repository/files/_data%2Fauthor%2Eyml/raw?ref=master'
    token: Optional[str] = getenv('BLOG_REPO_TOKEN')
    if token is None:
        raise ValueError('BLOG_REPO_TOKEN environment variable is not set')
    headers: Mapping[str, str | bytes] | None = {'PRIVATE-TOKEN': token}
    text_response = get(url, headers=headers).content.decode('utf-8')
    return safe_load(text_response)['main']['bio']


def posts() -> list[Post]:
    url = 'https://blog.frankel.ch/feed.xml'
    headers: Mapping[str, str | bytes] | None = {'User-Agent': 'Mozilla/5.0'}
    text_response: str = get(url, headers=headers).content.decode('utf-8')
    root: Element = ElementTree.fromstring(text_response)
    nodes: list[Element] = root.findall('./channel/item')[:3]

    def text_or_raise(node: Element, tag: str) -> str:
        result: Optional[Element] = node.find(tag)
        if result is None:
            raise ValueError(f'Could not find tag {tag}')
        text: Optional[str] = result.text
        if text is None:
            raise ValueError(f'Could not find text for {tag}')
        return text

    return [Post(datetime.strptime(text_or_raise(node, 'pubDate'), '%a, %d %b %Y %H:%M:%S %z'),
                 text_or_raise(node, 'title'),
                 text_or_raise(node, 'link'),
                 text_or_raise(node, 'description')) for node in nodes]


def talks() -> list[Talk]:
    confs_url = (f'https://gitlab.com/api/v4/projects/{blog_repo_path}/repository/files/_data%2Fconference%2Eyml/raw'
                 f'?ref=master')
    token: Optional[str] = getenv('BLOG_REPO_TOKEN')
    if token is None:
        raise ValueError('BLOG_REPO_TOKEN environment variable is not set')
    headers: Mapping[str, str | bytes] | None = {'PRIVATE-TOKEN': token}
    confs_text_response: str = get(confs_url, headers=headers).content.decode('utf-8')
    confs_yaml = safe_load(confs_text_response)
    only_confs = dict(filter(lambda conf: 'name' in conf[1], confs_yaml.items()))
    confs = {conf[0]: Conference(conf[1]['name'], conf[1].get('url', None))
             for conf in only_confs.items()}
    talks_url = f'https://gitlab.com/api/v4/projects/{blog_repo_path}/repository/files/_data%2Ftalk%2Eyml/raw?ref=master'
    talks_text_response: str = get(talks_url, headers=headers).content.decode('utf-8')
    talks_yaml = safe_load(talks_text_response)
    talks_raw = [(talk, node)
                 for node in talks_yaml
                 for talk in node['talks']]
    all_talks: list[Talk] = list(map(lambda talk: Talk(talk[0]['name'],
                                                       talk[0].get('url', None),
                                                       talk[0].get('description', None),
                                                       talk[1]['start-date'],
                                                       confs[talk[1]['conference']]), talks_raw))
    next_talks: list[Talk] = list(filter(lambda talk: talk.start_date > date.today(), all_talks))
    return sorted(next_talks, key=lambda talk: talk.start_date)[:3]


def video() -> Video:
    url = (f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=1'
           f'&playlistId=PL0EuBuKK-s1EL-K3okpYwR0QZbAPRVmEG&key={getenv("YOUTUBE_API_KEY")}')
    response = get(url).json()
    snippet = response['items'][0]['snippet']
    return Video(snippet['resourceId']['videoId'], snippet['title'])
