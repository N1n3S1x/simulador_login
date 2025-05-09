# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tela_principalWlUqbM.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTextBrowser, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(493, 477)
        self.pushButton_Login = QPushButton(Dialog)
        self.pushButton_Login.setObjectName(u"pushButton_Login")
        self.pushButton_Login.setGeometry(QRect(170, 160, 75, 24))
        self.pushButton_Registrar = QPushButton(Dialog)
        self.pushButton_Registrar.setObjectName(u"pushButton_Registrar")
        self.pushButton_Registrar.setGeometry(QRect(170, 190, 75, 24))
        self.lineEdit_Usuario = QLineEdit(Dialog)
        self.lineEdit_Usuario.setObjectName(u"lineEdit_Usuario")
        self.lineEdit_Usuario.setGeometry(QRect(150, 90, 113, 22))
        self.lineEdit_Senha = QLineEdit(Dialog)
        self.lineEdit_Senha.setObjectName(u"lineEdit_Senha")
        self.lineEdit_Senha.setGeometry(QRect(150, 120, 113, 22))
        self.textBrowser_Log = QTextBrowser(Dialog)
        self.textBrowser_Log.setObjectName(u"textBrowser_Log")
        self.textBrowser_Log.setGeometry(QRect(10, 270, 471, 192))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(100, 90, 49, 16))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(100, 120, 49, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Simulador de Login", None))
        self.pushButton_Login.setText(QCoreApplication.translate("Dialog", u"Login", None))
        self.pushButton_Registrar.setText(QCoreApplication.translate("Dialog", u"Registrar", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Usu\u00e1rio:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Senha:", None))
    # retranslateUi

