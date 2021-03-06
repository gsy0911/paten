.PHONY: help
help:
	@echo " == execute python test on some python .venv == "
	@echo "type 'make test-python' to execute python test with pytest"
	@echo ""
	@echo " == test-pypi upload == "
	@echo "type 'make clean wheel test-deploy' to upload test-pypi"
	@echo ""
	@echo " == pypi upload == "
	@echo "type 'make clean wheel deploy' to upload pypi"
	@echo ""
	@echo " == command references == "
	@echo "clean: clean build directory"
	@echo "wheel: build python project"
	@echo "deploy: upload to pypi"
	@echo "test-deploy: upload to pypi"
	@echo "test-python: test with pytest"

.PHONY: test-python
test-python:
	pytest ./test -vv --cov=./paten --cov-report=html

.PHONY: deploy
deploy:
	twine upload dist/*

.PHONY: test-deploy
test-deploy:
	twine upload -r testpypi dist/*

.PHONY: wheel
wheel:
	python setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -f -r paten.egg-info/* dist/* -y
