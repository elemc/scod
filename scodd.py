# main daemon script

from scoddaemon import SCODDaemon

if __name__ == '__main__':
	d = SCODDaemon()
	d.start_listen()
