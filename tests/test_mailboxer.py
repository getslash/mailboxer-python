from itertools import izip_longest


def test_get_mailboxes_empty(mailboxer):
    assert len(mailboxer.get_mailboxes()) == 0

def test_get_mailboxes_single_page(mailboxer, mailboxes):
    query = mailboxer.get_mailboxes(page_size=len(mailboxes) / 2)
    for mailbox, expected in izip_longest(query, mailboxes, fillvalue=None):
        assert mailbox.address == expected.address
    assert len(query) == len(mailboxes)
