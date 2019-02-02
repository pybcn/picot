import feedparser


def _ok_to_all_filter(x):
    return True


class Feed(object):
    def __init__(self, url, filter_func=None, format_func=None):
        if filter_func is None:
            filter_func = _ok_to_all_filter
        self.filter_func = filter_func
        self.format_func = format_func
        self._feed = feedparser.parse(url)
        self._entries = None

    def _update_entries(self):
        if self._entries is None:
            self._entries = [entry for entry in self._feed.entries if
                             self.filter_func(entry)]

    def __iter__(self):
        self._update_entries()
        return iter(self._entries)

    def __len__(self):
        self._update_entries()
        return len(self._entries)

    def __repr__(self):
        if self.format_func is None:
            return "{} ({})".format(
                self._feed.feed.title,
                self._feed.feed.link
            )
        return '\n'.join([self.format_func(entry) for entry in list(self)])
