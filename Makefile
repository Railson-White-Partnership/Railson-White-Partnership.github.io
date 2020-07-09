.PHONY: install
install:
	pip install pipenv
	pipenv install
.PHONY: test
test:
	pipenv run pytest
