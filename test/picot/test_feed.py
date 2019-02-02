import pytest

import feedparser

import picot.feed


class MockFeedProperty(object):
    entries = []
    link = ''
    title = ''


class MockFeed(object):
    def __init__(self, url, entries=None):
        if entries is None:
            entries = []
        self.entries = entries
        self.feed = MockFeedProperty()
        self.feed.link = url
        self.feed.title = 'Feed at {}'.format(url)


single_entry = [
    {
        'title': 'Some entry',
    },
]
multiple_entries = [
    {
        'title': 'Some entry',
    },
    {
        'title': 'Some other entry',
    },
]


@pytest.mark.parametrize(
    'expected_entries',
    [
        ([]),
        (single_entry),
        (multiple_entries),
    ],
    ids=[
        'No entries',
        'Single entry',
        'Multiple entries',
    ],
)
def test_feed(expected_entries, monkeypatch):
    def mocked_parse(url):
        return MockFeed(
            url,
            entries=expected_entries,
        )
    monkeypatch.setattr(feedparser, 'parse', mocked_parse)
    feed = picot.feed.Feed('https://some.url')
    assert(len(feed) == len(expected_entries))
    assert(repr(feed) == 'Feed at https://some.url (https://some.url)')
    for entry in feed:
        assert(len(entry) == len(expected_entries[0]))
        for expected_entry in expected_entries:
            for key in entry:
                if entry[key] == expected_entry[key]:
                    assert(entry[key] == expected_entry[key])
                    break


@pytest.mark.parametrize(
    'original_entries,filter_func,expected_entries',
    [
        (
            single_entry,
            None,
            single_entry,
        ),
        (
            single_entry,
            lambda x: False,
            [],
        ),
        (
            multiple_entries,
            lambda x: 'other' in x['title'],
            [
                {
                    'title': 'Some other entry',
                },
            ],
        ),
    ],
    ids=[
        'Single entry - No filter',
        'Single entry - Absolute filter',
        'Multiple entry - Filter some entries',
    ],
)
def test_feed_filter(
        original_entries,
        filter_func,
        expected_entries,
        monkeypatch,
):
    def mocked_parse(url):
        return MockFeed(
            url,
            entries=original_entries,
        )
    monkeypatch.setattr(feedparser, 'parse', mocked_parse)
    feed = picot.feed.Feed('https://some.url', filter_func=filter_func)
    assert(len(feed) == len(expected_entries))
    assert(list(feed) == expected_entries)


@pytest.mark.parametrize(
    'original_entries,format_func,expected_output',
    [
        (
            single_entry,
            None,
            'Feed at https://some.url (https://some.url)',
        ),
        (
            single_entry,
            lambda x: '',
            '',
        ),
        (
            single_entry,
            lambda x: x['title'],
            'Some entry',
        ),
        (
            multiple_entries,
            None,
            'Feed at https://some.url (https://some.url)',
        ),
        (
            multiple_entries,
            lambda x: '',
            '''\n''',
        ),
        (
            multiple_entries,
            lambda x: x['title'],
            'Some entry\nSome other entry',
        ),
    ],
    ids=[
        'Single entry - No format',
        'Single entry - Blank format',
        'Single entry - Simple format',
        'Multiple entry - No format',
        'Multiple entry - Blank format',
        'Multiple entry - Simple format',
    ],
)
def test_feed_format(
        original_entries,
        format_func,
        expected_output,
        monkeypatch,
):
    def mocked_parse(url):
        return MockFeed(
            url,
            entries=original_entries,
        )
    monkeypatch.setattr(feedparser, 'parse', mocked_parse)
    feed = picot.feed.Feed('https://some.url', format_func=format_func)
    assert(repr(feed) == expected_output)
