.PHONY: install
install:
	pip install pipenv
	pipenv install
.PHONY: test
test:
	pipenv run pytest --junit-xml=junit/test-results.xml
