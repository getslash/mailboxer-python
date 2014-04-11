
def test_get_mailboxes(mailboxer):
    assert len(mailboxer.get_mailboxes()) == 0
