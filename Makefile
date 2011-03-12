NAME        = scodd
#Commands
CP          = /bin/cp
INSTALL     = /usr/bin/install -D -p
RM          = /bin/rm -rf
MKDIR       = /bin/mkdir -p
# Dirs
DESTDIR     = /usr
SYSCONFDIR  = /etc
DATAROOTDIR = $(DESTDIR)/share/$(NAME)
BINDIR      = $(DESTDIR)/bin

# Code files
CODE_FILES  = nvidiaversion.py \
		scodcache.py \
		scodd.py \
		scoddaemon.py \
		scoddbusserver.py \
		scoddevice.py

all:
	@echo "This all, is a python source code. Type make install please."

clean:
	$(RM) *.pyc

uninstall:
	$(RM) $(SYSCONFDIR)/$(NAME)
	$(RM) $(DATAROOTDIR)
	$(RM) $(BINDIR)/$(NAME)

install: install-sysconf $(CODE_FILES)
	$(INSTALL) -m 755 scodd.sh $(BINDIR)/scodd

mk-sysconfdir:
	$(MKDIR) $(SYSCONFDIR)/$(NAME)

install-sysconf: mk-sysconfdir
	$(INSTALL) -m 644 devices.conf $(SYSCONFDIR)/$(NAME)

mk-dataroot:
	$(MKDIR) $(DATAROOTDIR)

$(CODE_FILES): mk-dataroot
	$(INSTALL) -m 644 $@ $(DATAROOTDIR)/$@