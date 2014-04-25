import os
import shutil
import subprocess
import sys
import tempfile
import uuid

from urlobject import URLObject as URL
from flask_loopback import FlaskLoopback

import pytest
from mailboxer import Mailboxer

sys.path.insert(0, os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "..", ".env", "mailboxer"))
from flask_app.app import app
from flask_app import models

def pytest_addoption(parser):
    parser.addoption("--setup-db", action="store_true", default=False)

@pytest.fixture(scope="session")
def db_engine(request):
    if request.config.getoption("--setup-db"):
        tmpdir = tempfile.mkdtemp()
        subprocess.check_call("pg_ctl init -D {0} -w".format(tmpdir), shell=True)
        subprocess.check_call("pg_ctl start -D {0} -w".format(tmpdir), shell=True)
        @request.addfinalizer
        def finalize():
            subprocess.check_call("pg_ctl stop -D {0} -w -m immediate".format(tmpdir), shell=True)
            shutil.rmtree(tmpdir)

        subprocess.check_call("createdb mailboxer", shell=True)

    models.db.session.close()
    models.db.drop_all()
    models.db.create_all()


@pytest.fixture(scope="session")
def mailboxer_url(request, db_engine):
    loopback = FlaskLoopback(app)
    hostname = str(uuid.uuid1())
    loopback.activate_address((hostname, 80))
    @request.addfinalizer
    def close():
        loopback.deactivate_address((hostname, 80))
    return URL("http://{0}".format(hostname))

@pytest.fixture
def mailboxer(mailboxer_url):
    return Mailboxer(mailboxer_url)

@pytest.fixture(
    params=[10]
    )
def num_objects(request):
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
        for i in range(num_objects)]
