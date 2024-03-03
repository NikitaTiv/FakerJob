style:
	flake8 .

types:
	mypy .

test:
	./manage.py test

check:
	make style types test
