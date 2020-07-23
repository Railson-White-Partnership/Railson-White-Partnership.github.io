.PHONY: install
install:
	pip install pipenv
	pipenv install
	gem install bundler
	bundle install
.PHONY: localserver
localserver:
	bundle exec jekyll serve &
.PHONY: test
test:
	pipenv run pytest --junit-xml=test-reports/test-results.xml
