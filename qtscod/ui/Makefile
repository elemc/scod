UI=MainWindow
PYUIC=/usr/bin/pyuic4
MAKEPY=$(PYUIC) -o

all: clean $(UI).py
	@echo "Done"

clean:
	rm -rf *.py
	touch __init__.py

$(UI).py:
	$(MAKEPY) $@ ui/$(UI).ui
