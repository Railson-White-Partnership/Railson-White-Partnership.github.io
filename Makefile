.PHONY: install
install:
	pip install pipenv
	pipenv install
	gem install jekyll bundler
.PHONY: test
test:
	pipenv run pytest --junit-xml=test-reports/test-results.xml
