.PHONY: install
install:
	pip install pipenv
	pipenv install
	gem install jekyll bundler
.PHONY: localserver
localserver:
	bundle exec jekyll serve &
.PHONY: test
test:
	pipenv run pytest --junit-xml=test-reports/test-results.xml
