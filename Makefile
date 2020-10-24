.PHONY: clean
clean:
	-@rm -rf build dist pstream.egg-info coverage.xml .coverage .pytest_cache

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: release
release:
	python -m twine upload --repository pypi -u __token__ --verbose -p ${PYPI_TOKEN} dist/*

.PHONY: test
test:
	python3 -m pytest --cov=pstream -W error --cov-report=xml --cov-branch tests
	python3 -m flake8 pstream tests --extend-ignore=F405,E501,F403,F401 --exclude functors.py
	# functors.py does imports in the middle of the file because in its case it actually
	# makes the whole thing easier to read. So let E402 slide on that one file.
	python3 -m flake8 pstream/_async/functors.py --extend-ignore=F405,E501,F403,F401,E402

.PHONY: test
test_html:
	python3 -m pytest --cov=pstream -W error --cov-report=html --cov-branch tests
	python3 -m flake8 pstream tests --extend-ignore=F405,E501,F403,F401 --exclude functors.py
	# functors.py does imports in the middle of the file because in its case it actually
	# makes the whole thing easier to read. So let E402 slide on that one file.
	python3 -m flake8 pstream/_async/functors.py --extend-ignore=F405,E501,F403,F401,E402

.PHONY: testpy2
testpy2:
	python -m pytest --cov=pstream -W error --cov-report=xml --cov-branch tests/sync
	python -m flake8 pstream/_sync/*.py pstream/utils/*.py pstream/errors.py tests/sync/*.py --extend-ignore=F405,E501,F403,F401
