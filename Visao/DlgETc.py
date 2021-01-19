# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgETc.ui'
#
# Created: Wed Nov 11 00:58:52 2015
#      by: PyQt5 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Controle.ConEtc import Controller

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


# try:
#     _encoding = QtGui.QApplication.UnicodeUTF8
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig, _encoding)
# except AttributeError:
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig)


def _translate(context, text, disambig):
    return text


class Ui_Dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        try:
            self.controller = Controller(self)

            Dialog.resize(371, 290)
            self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
            self.gridLayout = QtWidgets.QGridLayout()
            self.verticalLayout.addLayout(self.gridLayout)

            self.rbEtc = QtWidgets.QRadioButton(Dialog)
            self.gridLayout.addWidget(self.rbEtc, 0, 0, 1, 1)
            self.rbEtc.setChecked(True)

            self.rbEta = QtWidgets.QRadioButton(Dialog)
            self.gridLayout.addWidget(self.rbEta, 0, 1, 1, 1)

            self.label = QtWidgets.QLabel(Dialog)
            self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

            self.label_2 = QtWidgets.QLabel(Dialog)
            self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

            self.btnConfET0 = QtWidgets.QPushButton(Dialog)
            self.gridLayout.addWidget(self.btnConfET0, 2, 1, 1, 1)

            self.chET0 = QtWidgets.QCheckBox(Dialog)
            self.chET0.setEnabled(False)
            self.gridLayout.addWidget(self.chET0, 2, 2, 1, 1)

            self.label_3 = QtWidgets.QLabel(Dialog)
            self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

            self.btnConfKc = QtWidgets.QPushButton(Dialog)
            self.gridLayout.addWidget(self.btnConfKc, 3, 1, 1, 1)

            self.chKc = QtWidgets.QCheckBox(Dialog)
            self.chKc.setEnabled(False)
            self.gridLayout.addWidget(self.chKc, 3, 2, 1, 1)

            self.label_4 = QtWidgets.QLabel(Dialog)
            self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

            self.label_5 = QtWidgets.QLabel(Dialog)
            self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

            self.btnConfETc = QtWidgets.QPushButton(Dialog)
            self.gridLayout.addWidget(self.btnConfETc, 5, 1, 1, 1)

            self.chETc = QtWidgets.QCheckBox(Dialog)
            self.chETc.setEnabled(False)
            self.gridLayout.addWidget(self.chETc, 5, 2, 1, 1)

            spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)

            self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
            self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

            self.verticalLayout.addWidget(self.buttonBox)

            self.retranslateUi(Dialog)
            self.buttonBox.accepted.connect(self.controller.action_ok)
            self.buttonBox.rejected.connect(self.controller.action_cancel)
            QtCore.QMetaObject.connectSlotsByName(Dialog)

            self.btnConfET0.clicked.connect(self.controller.setSerieET0)
            self.btnConfKc.clicked.connect(self.controller.setSerie_Kc)
            self.btnConfETc.clicked.connect(self.controller.setSerie_ETc)

            self.rbEta.clicked.connect(self.controller.MudaPraETa)
            self.rbEtc.clicked.connect(self.controller.MudaPraETc)

        except Exception as e:
            print(e)


        self.controller.parametros_teste()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "CyMP - Evapotranspiração", None))
        self.label_4.setText(_translate("Dialog", "Configuração de saída:", None))
        self.label_5.setText(_translate("Dialog", "Imagens diárias de ETc", None))
        self.btnConfETc.setText(_translate("Dialog", "Configurar", None))
        self.chETc.setText(_translate("Dialog", "Configurado", None))
        self.label.setText(_translate("Dialog", "Configuração de entrada", None))
        self.label_2.setText(_translate("Dialog", "Imagens diárias de ET0", None))
        self.btnConfET0.setText(_translate("Dialog", "Configurar", None))
        self.chET0.setText(_translate("Dialog", "Configurado", None))
        self.label_3.setText(_translate("Dialog", "Imagens diárias de Kc", None))
        self.btnConfKc.setText(_translate("Dialog", "Configurar", None))
        self.chKc.setText(_translate("Dialog", "Configurado", None))

        self.rbEta.setText(_translate("Dialog", "ETa (FAO)", None))
        self.rbEtc.setText(_translate("Dialog", "ETc", None))
