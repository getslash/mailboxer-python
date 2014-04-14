import json
import requests
from urlobject import URLObject as URL

from .query import Query


class Mailboxer(object):

    def __init__(self, url):
        super(Mailboxer, self).__init__()
        self.url = URL(url).add_path("v2")

    def create_mailbox(self, address):
        self._post(self.url.add_path("mailboxes"), {"address": address})
        return Mailbox(self, address)

    def get_emails(self, address):
        return self.get_mailbox(address).get_emails()

    def get_mailboxes(self, **kwargs):
        return Query(self, self.url.add_path("mailboxes"), Mailbox, **kwargs)

    def get_mailbox(self, address):
        return Mailbox(self, address)

    def _post(self, url, data):
        resp = requests.post(url, data=json.dumps(data),
                             headers={"Content-type": "application/json"})

    def _get_paged(self, url, obj):
        return [obj(data) for data in requests.get(url).json()["result"]]

    def _mailbox_url(self, address):
        return self.url.add_path("mailboxes").add_path(address)

class Mailbox(object):

    def __init__(self, mailboxer, address):
        super(Mailbox, self).__init__()
        self.mailboxer = mailboxer
        self.address = address
        self.url = self.mailboxer.url.add_path("mailboxes").add_path(self.address)

    @classmethod
    def from_query_json(cls, mailboxer, json):
        return cls(mailboxer, json["address"])

    def get_emails(self):
        return self.mailboxer._get_paged(self.url.add_path("emails"), Email)

class Email(object):

    def __init__(self, email_dict):
        super(Email, self).__init__()
        self.__dict__.update(email_dict)
