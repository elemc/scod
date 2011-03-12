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
DBUS_DIR    = $(SYSCONFDIR)/dbus-1/system.d

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
	$(RM) $(DBUS_DIR)/$(NAME).conf

install: install-sysconf $(CODE_FILES)
	$(INSTALL) -m 755 $(NAME).sh $(BINDIR)/$(NAME)
	$(INSTALL) -m 644 $(NAME).conf $(DBUS_DIR)/$(NAME).conf

mk-sysconfdir:
	$(MKDIR) $(SYSCONFDIR)/$(NAME)
	$(MKDIR) $(DBUS_DIR)

install-sysconf: mk-sysconfdir
	$(INSTALL) -m 644 devices.conf $(SYSCONFDIR)/$(NAME)

mk-dataroot:
	$(MKDIR) $(DATAROOTDIR)

$(CODE_FILES): mk-dataroot
	$(INSTALL) -m 644 $@ $(DATAROOTDIR)/$@