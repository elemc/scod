#!/usr/bin/env python

# Qt4
from PyQt4 import QtCore
from PyQt4.QtCore import QObject, QTranslator, QLibraryInfo, QLocale
from PyQt4.QtGui import QApplication

# Forms
from src.MainWindow import MainWindow
#from src.ListenThread import ListenThread

# sys
import sys

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setOrganizationName( "RussianFedora" )
	app.setOrganizationDomain( "www.russianfedora.ru" )
	app.setApplicationName( "Qt SCOD Client" )
	
	locale = QLocale.system()
	
	trans_path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
	translator = QTranslator(app)
	translator.load( "qt_%s" % locale.languageToString(locale.language()),  trans_path)
	app.installTranslator(translator)

	
	w = MainWindow()
	w.hide()
	#t = ListenThread(w)
	#t.start()
	#w.show()
	w.start_listen()
	sys.exit(app.exec_())
