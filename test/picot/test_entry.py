import pytest

import picot.entry


raw_entry = {
    'title': 'Some entry',
    'link': 'https://some.site/entry',
}


@pytest.mark.parametrize(
    'format_func,expected_output',
    [
        (
            None,
            repr(raw_entry),
        ),
        (
            lambda x: x['title'],
            raw_entry['title'],
        ),
        (
            lambda x: '{} {}'.format(x['title'], x['link']),
            '{} {}'.format(raw_entry['title'], raw_entry['link']),
        ),
    ],
    ids=[
        'No format function',
        'Simple format function',
        'Field combining format function',
    ],
)
def test_entry_format(
        format_func,
        expected_output,
):
    entry = picot.entry.Entry(raw_entry, format_func=format_func)
    assert(repr(entry) == expected_output)
