# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interpoladorECMWF_Demo.ui'
#
# Created: Fri Mar 06 22:12:54 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import InterpoladorECMWF_Demo_Controller
from PyQt4.QtGui import *

 
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self, controller):
        self.controller = controller
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        
        
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(436, 361)
        self.leShapePath = QtGui.QLineEdit(Form)
        self.leShapePath.setGeometry(QtCore.QRect(10, 40, 301, 20))
        self.leShapePath.setObjectName(_fromUtf8("leShapePath"))
        self.cbAtribute = QtGui.QComboBox(Form)
        self.cbAtribute.setEnabled(False)
        self.cbAtribute.setGeometry(QtCore.QRect(10, 90, 331, 22))
        self.cbAtribute.setObjectName(_fromUtf8("cbAtribute"))
        self.btnFindShp = QtGui.QPushButton(Form)
        self.btnFindShp.setGeometry(QtCore.QRect(330, 40, 75, 23))
        self.btnFindShp.setObjectName(_fromUtf8("btnFindShp"))
        self.bbOkCancela = QtGui.QDialogButtonBox(Form)
        self.bbOkCancela.setGeometry(QtCore.QRect(190, 330, 156, 23))
        self.bbOkCancela.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbOkCancela.setObjectName(_fromUtf8("bbOkCancela"))
        self.lwGroupAtributes = QtGui.QListWidget(Form)
        self.lwGroupAtributes.setEnabled(False)
        self.lwGroupAtributes.setGeometry(QtCore.QRect(10, 230, 331, 71))
        self.lwGroupAtributes.setObjectName(_fromUtf8("lwGroupAtributes"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 200, 161, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 131, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayoutWidget = QtGui.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(120, 40, 2, 2))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 130, 111, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.leImgRefPath = QtGui.QLineEdit(Form)
        self.leImgRefPath.setGeometry(QtCore.QRect(10, 150, 301, 20))
        self.leImgRefPath.setObjectName(_fromUtf8("leImgRefPath"))
        self.btnFindImgRef = QtGui.QPushButton(Form)
        self.btnFindImgRef.setGeometry(QtCore.QRect(330, 150, 75, 23))
        self.btnFindImgRef.setObjectName(_fromUtf8("btnFindImgRef"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Gafanhoto Beta 0.01 - Interpolador ECMWF", None))
        self.btnFindShp.setText(_translate("Form", "Procurar", None))
        self.label_2.setText(_translate("Form", "Agrupar dados pelor atributos:", None))
        self.label_3.setText(_translate("Form", "Atributo a ser interpolado", None))
        self.label.setText(_translate("Form", "Shape ECMWF", None))
        self.label_4.setText(_translate("Form", "Imagem de referencia", None))
        self.btnFindImgRef.setText(_translate("Form", "Procurar", None))
        
        self.btnFindShp.clicked.connect(self.controller.btn_FindShp_ClickAction)
        self.btnFindImgRef.clicked.connect(self.controller.btn_FindImgRef_ClickAction)
        self.bbOkCancela.buttons()[0].clicked.connect(self.controller.btn_OK_ClickAction)
        self.bbOkCancela.buttons()[1].clicked.connect(self.controller.btn_Cancel_ClickAction)
        self.leShapePath.textChanged.connect(self.controller.le_shapePath_ChangeAction)
        self.leImgRefPath.textChanged.connect(self.controller.le_imgRefPath_ChangeAction)
        self.cbAtribute.currentIndexChanged.connect(self.controller.cb_Atribute_ChangeAction)
        
    def contextMenuEvent(self, event):
         
        menu = QMenu(self)
        
        quitAction = menu.addAction("Quit")
        
        action = menu.exec_(self.mapToGlobal(event.pos()))
        
        if action == quitAction:
            qApp.quit()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    controller = InterpoladorECMWF_Demo_Controller.InterpoladorECMWF_Demo_Controller()

    ex = Ui_Form(controller)
    controller.form = ex
    
    ex.show()
    sys.exit(app.exec_())