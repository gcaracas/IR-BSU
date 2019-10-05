SRCDIR   := $(shell pwd)
ROOT_DIR   := $(shell basename $(SRCDIR))

all: clean deps build


clean:
	@-rm -f logs/*.log

deps: venv
	@-mkdir logs

prepare-dev-centos:
	sudo yum -y install python3 python3-pip
	python3 -m pip install virtualenv
	make venv

prepare-dev-ubuntu:
	sudo apt-get -y install python3 python3-pip
	python3 -m pip install virtualenv
	make venv

prepare-dev-mac:
	brew list python3 &>/dev/null || brew install python3
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python3 get-pip.py
	python3 -m pip install virtualenv
	make venv

venv: activate_venv

activate_venv: requirements.txt
	test -d venv || virtualenv -p python3 venv
	venv/bin/python -m pip install -U pip
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

run: deps
	source venv/bin/activate ; python Indexing.py

rel: deps
	source venv/bin/activate ; python relevance_ranking.py

