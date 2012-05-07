CLEANFILES = $(shell find . -type f -name '*.py[oc]')
CLEANDIRS = dist locale

.PHONY: bundle test 

all:
	python setup.py build

bundle:
	./createbundle.sh

test:
	./testcases/runtests.sh

clean:
	@rm -rf $(addprefix ./,$(CLEANDIRS))
	@rm -rf $(addprefix ./,$(CLEANFILES))

run:
	python main.py
