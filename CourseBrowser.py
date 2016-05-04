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

class SecondScreen(object):
    def setupUi(self, FirstScreen):
        self.buttonList = []
        self.FirstScreen = FirstScreen
        self.label = QtGui.QLabel(FirstScreen)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.backButton = QtGui.QPushButton("Back", FirstScreen)
        self.retranslateUi(FirstScreen)
        print "Course Browser Added"

    def retranslateUi(self, FirstScreen):
        self.label.setText(_translate("FirstScreen", "Your Courses", None))
        self.label.setGeometry(QtCore.QRect(0, 26, 180, 51))
        self.backButton.setGeometry(QtCore.QRect(0, 0, 80, 25))
        self.backButton.show()
        self.label.show()

    def remove(self):
        self.label.close()
        self.backButton.close()
        for button in self.buttonList:
            button.close()
            #self.buttonList.remove(button)
        self.buttonList = []

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FirstScreen = QtGui.QWidget()
    ui = SecondScreen()
    ui.setupUi(FirstScreen)
    FirstScreen.show()
    sys.exit(app.exec_())

