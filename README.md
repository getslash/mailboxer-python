
![Build Status] (https://secure.travis-ci.org/vmalloc/mailboxer-python.png )


![Downloads] (https://pypip.in/d/mailboxer-python/badge.png )

![Version] (https://pypip.in/v/mailboxer-python/badge.png )

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

