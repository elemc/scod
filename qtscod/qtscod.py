#!/usr/bin/env python

# Qt4
from PyQt4 import QtCore
from PyQt4.QtCore import QObject, QTranslator, QLibraryInfo, QLocale, QString
from PyQt4.QtGui import QApplication

# Forms
from src.MainWindow import MainWindow
#from src.ListenThread import ListenThread

# sys
import sys

def get_lang_code(full_lang_name):
	llang = str(full_lang_name).split('_')
	if len(llang) > 1:
		return llang[0]
	return None

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setOrganizationName( "RussianFedora" )
	app.setOrganizationDomain( "www.russianfedora.ru" )
	app.setApplicationName( "Qt SCOD Client" )
	
	locale = QLocale.system()
	
	trans_path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
	translator = QTranslator(app)
	lang = get_lang_code(locale.name())
	if lang is not None:
		trans_file = QString("qt_%s" % lang)
		#print trans_file
		translator.load(trans_file ,  trans_path)
		app.installTranslator(translator)

	
	w = MainWindow()
	#w.hide()
	w.start_listen()
	sys.exit(app.exec_())
