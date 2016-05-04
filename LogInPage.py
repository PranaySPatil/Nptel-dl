__author__ = 'Pranay'

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firstscreen.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class FirstScreen(object):
    def setupUi(self, FirstScreen):
        FirstScreen.setObjectName(_fromUtf8("FirstScreen"))
        self.eMail = QtGui.QLineEdit(FirstScreen)
        self.eMail.setGeometry(QtCore.QRect(60, 40, 113, 20))
        self.eMail.setObjectName(_fromUtf8("eMail"))
        self.passWd = QtGui.QLineEdit(FirstScreen)
        self.passWd.setGeometry(QtCore.QRect(60, 140, 113, 20))
        self.passWd.setEchoMode(QtGui.QLineEdit.Password)
        self.passWd.setObjectName(_fromUtf8("passWd"))
        self.SignInButton = QtGui.QPushButton(FirstScreen)
        self.SignInButton.setGeometry(QtCore.QRect(240, 220, 101, 51))
        self.SignInButton.setObjectName(_fromUtf8("SignInButton"))

        self.retranslateUi(FirstScreen)
        QtCore.QMetaObject.connectSlotsByName(FirstScreen)

    def retranslateUi(self, FirstScreen):
        self.eMail.setPlaceholderText(_translate("FirstScreen", "Email ID", None))
        self.passWd.setPlaceholderText(_translate("FirstScreen", "Password", None))
        self.SignInButton.setText(_translate("FirstScreen", "Sign In", None))
        self.eMail.show()
        self.passWd.show()
        self.SignInButton.show()

    def remove(self):
        self.eMail.close()
        self.passWd.close()
        self.SignInButton.close()
        print "SignIn page removed"

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FirstScreen = QtGui.QWidget()
    ui = FirstScreen()
    ui.setupUi(FirstScreen)
    FirstScreen.show()
    sys.exit(app.exec_())

