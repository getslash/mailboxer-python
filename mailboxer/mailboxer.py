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

    def delete_mailbox(self, address):
        return self.get_mailbox(address).delete()

    def get_emails(self, address, unread = False):
        return self.get_mailbox(address).get_emails(unread)

    def get_mailboxes(self, **kwargs):
        return Query(self, self.url.add_path("mailboxes"), Mailbox, **kwargs)

    def get_mailbox(self, address):
        return Mailbox(self, address)

    def does_mailbox_exist(self, address):
        return Mailbox(self, address).exists()

    def _post(self, url, data):
        returned = requests.post(url, data=json.dumps(data),
                      headers={"Content-type": "application/json"})
        returned.raise_for_status()
        return returned

    def _get_paged(self, url, obj):
        resp = requests.get(url)
        resp.raise_for_status()
        return [obj(data) for data in resp.json()["result"]]

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

    def get_emails(self, unread = False):
        url = self.url.add_path("unread_emails") if unread else self.url.add_path("emails")
        return self.mailboxer._get_paged(url, Email)

    def exists(self):
        url = self.url.add_path("emails")
        response = requests.get(url)
        if(response.status_code == requests.codes.not_found):
            return False
        response.raise_for_status()
        return True

    def delete(self):
        requests.delete(self.url).raise_for_status()

class Email(object):

    def __init__(self, email_dict):
        super(Email, self).__init__()
        self.__dict__.update(email_dict)
