import feedparser

class Feed(object):
    def __init__(self, url, filter_func=None):
        if filter_func is None:
            filter_func = lambda x: True
        self.filter_func = filter_func
        self._feed = feedparser.parse(url)
        self._entries = None

    def _update_entries(self):
        if self._entries is None:
            self._entries = [entry for entry in self._feed.entries if self.filter_func(entry)]

    def __iter__(self):
        self._update_entries()
        return iter(self._entries)

    def __len__(self):
        self._update_entries()
        return len(self._entries)

    def __repr__(self):
        return "{} ({})".format(
            self._feed.feed.title,
            self._feed.feed.link
        )
