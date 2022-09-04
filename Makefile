flake8:
	flake8 .

e2e-tests:
	pytest test $(args)