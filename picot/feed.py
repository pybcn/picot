import feedparser

class Feed(object):
    def __init__(self, url):
        self._feed = feedparser.parse(url)

    def __iter__(self):
        return iter(self._feed.entries)

    def __len__(self):
        return len(self._feed.entries)

    def __repr__(self):
        return "{} ({})".format(
            self._feed.feed.title,
            self._feed.feed.link
        )
