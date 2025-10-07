import json
import requests
from urlobject import URLObject as URL

from .query import Query


class Mailboxer:
    def __init__(self, url):
        super().__init__()
        self.url = URL(url).add_path("v2")

    def create_mailbox(self, address):
        self._post(self.url.add_path("mailboxes"), {"address": address})
        return Mailbox(self, address)

    def delete_mailbox(self, address):
        return self.get_mailbox(address).delete()

    def get_emails(self, address, unread=False):
        return self.get_mailbox(address).get_emails(unread)

    def get_mailboxes(self, **kwargs):
        return Query(self, self.url.add_path("mailboxes"), Mailbox, **kwargs)

    def get_mailbox(self, address):
        return Mailbox(self, address)

    def does_mailbox_exist(self, address):
        return Mailbox(self, address).exists()

    def _post(self, url, data):
        returned = requests.post(
            url,
            data=json.dumps(data),
            headers={"Content-type": "application/json"},
            timeout=30,
        )
        returned.raise_for_status()
        return returned

    def _get_paged(self, url, obj):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return [obj(data) for data in response.json()["result"]]

    def _mailbox_url(self, address):
        return self.url.add_path("mailboxes").add_path(address)


class Mailbox:
    def __init__(self, mailboxer, address):
        super().__init__()
        self.mailboxer = mailboxer
        self.address = address
        self.url = self.mailboxer.url.add_path("mailboxes").add_path(self.address)

    @classmethod
    def from_query_json(cls, mailboxer, json):  # pylint: disable=redefined-outer-name
        return cls(mailboxer, json["address"])

    def get_emails(self, unread=False):
        url = (
            self.url.add_path("unread_emails")
            if unread
            else self.url.add_path("emails")
        )
        return self.mailboxer._get_paged(url, Email)  # pylint: disable=protected-access

    def exists(self):
        url = self.url.add_path("emails")
        response = requests.get(url, timeout=30)
        if response.status_code == requests.codes.not_found:  # pylint: disable=no-member
            return False
        response.raise_for_status()
        return True

    def delete(self):
        requests.delete(self.url, timeout=30).raise_for_status()


class Email:
    def __init__(self, email_dict):
        super().__init__()
        self.__dict__.update(email_dict)
