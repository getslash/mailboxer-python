default: test

test: env
	.env/bin/pytest -x tests

travis_test: env
	PYTHONPATH=.env/mailboxer .env/bin/pytest

env: .env/.up-to-date


.env/.up-to-date: setup.py Makefile
	virtualenv --no-site-packages .env
	.env/bin/pip install -e ".[testing]"
	test -d .env/mailboxer || git clone https://github.com/vmalloc/mailboxer .env/mailboxer
	.env/bin/pip install -r .env/mailboxer/deps/base.txt -r .env/mailboxer/deps/develop.txt -r .env/mailboxer/deps/app.txt
	touch $@

