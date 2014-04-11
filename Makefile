default: test

test: env
	.env/bin/py.test -x tests

travis_test: env
	.env/bin/py.test --no-setup-db

env: .env/.up-to-date


.env/.up-to-date: setup.py Makefile
	virtualenv --no-site-packages .env
	.env/bin/pip install -e .
	.env/bin/pip install -r ./mailboxer_python.egg-info/requires.txt
	.env/bin/pip install pytest Flask-Loopback
	test -d .env/mailboxer || git clone https://github.com/vmalloc/mailboxer .env/mailboxer
	.env/bin/pip install -r .env/mailboxer/base_requirements.txt
	.env/bin/pip install -r .env/mailboxer/flask_app/pip_requirements.txt
	touch $@

