NAME        = qtscod
#Commands
CP          = /bin/cp
INSTALL     = /usr/bin/install -D -p
RM          = /bin/rm -rf
MKDIR       = /bin/mkdir -p
# Dirs
DESTDIR     = /usr
DATAROOTDIR = $(DESTDIR)/share/$(NAME)
BINDIR      = $(DESTDIR)/bin
PYUIC	    = /usr/bin/pyuic4
MAKEUIPY    = $(PYUIC) -o

# Code files
CODE_FILES  = packagekitwrapper.py \
		qtscod.py \
		src/ActionsModel.py \
		src/Device.py \
		src/DevicesListModel.py \
		src/__init__.py \
		src/KernelVariant.py \
		src/ListenThread.py \
		src/MainWindow.py \
		ui/__init__.py

UI_FILES    = ui/MainWindow

IMG_FILES   = img/apply.png \
		img/cancelactions.png \
		img/deleteaction.png \
		img/disableall.png \
		img/disable.png \
		img/gears.svg \
		img/hardware.svg \
		img/wifi.svg

all:
	@echo "This all, is a python source code. Type make install please."

clean:
	$(RM) *.pyc

uninstall:
	$(RM) $(DATAROOTDIR)
	$(RM) $(BINDIR)/$(NAME)

install: $(CODE_FILES) $(IMG_FILES)
	$(INSTALL) -m 755 ../tools/$(NAME).sh $(BINDIR)/$(NAME)

mk-dataroot: 
	$(MKDIR) $(DATAROOTDIR)/ui $(DATAROOTDIR)/src $(DATAROOTDIR)/img
	touch ui/__init__.py

$(CODE_FILES): mk-dataroot $(UI_FILES).py
	$(INSTALL) -m 644 $@ $(DATAROOTDIR)/$@

$(UI_FILES).py:
	$(MAKEUIPY) $@ ui/$(UI_FILES).ui
	$(INSTALL) -m 644 $@ $(DATAROOTDIR)/$@

$(IMG_FILES): mk-dataroot
	$(INSTALL) -m 644 ../$@ $(DATAROOTDIR)/$@
