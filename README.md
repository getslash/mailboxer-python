
![Build Status] (https://secure.travis-ci.org/getslash/mailboxer-python.png )

![Version] (https://img.shields.io/pypi/v/mailboxer-python.svg )

Overview
========

`mailboxer-python` is a client library for [the Mailboxer webapp](https://github.com/vmalloc/mailboxer ). It provides Pythonic wrapping of the API exposed by Mailboxer.


Getting Started
===============

1. Install mailboxer-python:

	```
	$ pip install mailboxer-python
	```

2. Start using it:

	```
	>>> from mailboxer improt Mailboxer
	>>> m = Mailboxer("http://my.mailboxer.hostname")
	>>> mailbox = m.create_mailbox("recipient@somedomain.com")
	>>> emails = mailbox.get_emails()
	```

Documentation
=============

** Coming Soon **
										   

Licence
=======

BSD3

