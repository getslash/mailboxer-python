import uuid

from urlobject import URLObject as URL
from flask_loopback import FlaskLoopback

import pytest
from mailboxer import Mailboxer

from .flask_app import create_app, app_initializations


@pytest.fixture(scope="session", name="mailboxer_url")
def mailboxer_url_fx():
    app = create_app()
    loopback = FlaskLoopback(app)
    hostname = str(uuid.uuid1())
    port = 80
    loopback.activate_address((hostname, port))
    with app.app_context():
        app_initializations()
        yield URL(f"http://{hostname}:{port}")
        loopback.deactivate_address((hostname, port))


@pytest.fixture(name="mailboxer")
def mailboxer_fx(mailboxer_url):
    return Mailboxer(mailboxer_url)


@pytest.fixture(params=[10], name="num_objects")
def num_objects_fx(request):
    return request.param


@pytest.fixture
def mailbox(request, mailboxer):
    returned = mailboxer.create_mailbox("mailbox@mailboxer.com")
    request.addfinalizer(returned.delete)
    return returned


@pytest.fixture
def mailboxes(mailboxer, num_objects):
    return [
        mailboxer.create_mailbox("mailbox{0}@mailboxer.com".format(i))
        for i in range(num_objects)
    ]
