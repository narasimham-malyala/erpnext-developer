include .env

PACKAGE     = bench

VIRTUALENV := virtualenv

BASEDIR     = $(realpath .)
VENVDIR     = $(BASEDIR)/.venv

ifeq ($(PYTHON_ENVIRONMENT),2)
VENV	   := $(VENVDIR)/py2
SYSPYTHON  := $(shell which python2)
else
VENV       := $(VENVDIR)/py3
SYSPYTHON  := $(shell which python3)
endif

VENVBIN     = $(VENV)/bin
PYTHON      = $(VENVBIN)/python
PIP         = $(VENVBIN)/pip
IPYTHON     = $(VENVBIN)/ipython

PYTEST      = $(VENVBIN)/pytest
CANIUSEPY3  = $(VENVBIN)/caniusepython3

venv:
	$(VIRTUALENV) $(VENV) --python $(SYSPYTHON)

clean:
	find $(BASEDIR) | grep -E "__pycache__|\.pyc" | xargs rm -rf

	rm -rf $(BASEDIR)/$(PACKAGE).egg-info $(BASEIDR)/build $(BASEDIR)/dist

	clear

install:
	cat requirements/*.txt          > requirements-dev.txt
	cat requirements/production.txt > requirements.txt

	$(PIP) install -r $(BASEDIR)/requirements-dev.txt

	$(PYTHON) setup.py install

	make clean

check.py3:
	$(CANIUSEPY3) --requirements $(BASEDIR)/requirements-dev.txt

test:
	$(PYTEST)

console:
	$(IPYTHON)