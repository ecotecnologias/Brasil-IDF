# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BrasilIDFDialog
                                 A QGIS plugin
 FAZER A DESCRIÇÃO
                             -------------------
        begin                : 2016-10-03
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Ecotecnologias
        email                : robsonleopachaly@yahoo.com.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic, QtCore

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'brasil_IDF_dialog_base.ui'))


class BrasilIDFDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
               
        super(BrasilIDFDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        
        #Deixa o plugin sempre em cima de todos os programas do computador
        #QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        
        
        self.setupUi(self)

