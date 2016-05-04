from functools import partial

__author__ = 'Pranay'
import sys
from PyQt4 import QtGui, QtCore
from LogInPage import FirstScreen
from CourseBrowser import SecondScreen
from CourseContentPage import ThirdScreen
from nptel_dl import NPTEL_DL

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle("NPTEL")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.firstScreen = FirstScreen()
        self.secondScreen = SecondScreen()
        self.thirdScreen = ThirdScreen()
        self.LoadSignInPage()
        self.nptel = NPTEL_DL()

    def LoadCoursePage(self):
        self.secondScreen.setupUi(self)
        self.secondScreen.backButton.clicked.connect(self.back_to_signin)
        self.loadCourses()
        self.update()

    def LoadSignInPage(self):
        self.firstScreen.setupUi(self)
        self.firstScreen.SignInButton.clicked.connect(self.signin)
        self.update()

    def LoadCourseContentPage(self):
        self.thirdScreen.setupUi(self)
        self.thirdScreen.backButton.clicked.connect(self.back_to_coursePage)
        self.thirdScreen.downloadAllButton.clicked.connect(self.download_all_videos)
        self.populate_course_content()
        self.update()

    def signin(self):
        # user = self.firstScreen.eMail.text()
        # passWd = self.firstScreen.passWd.text()
        user = "pranay.patil0@gmail.com"
        passWd = "Pr@nay007"
        response_code, response_url = self.nptel.sign_in(user, passWd)
        self.msgBox = QtGui.QMessageBox(self)
        if response_code == 200:
            if response_url.find(self.nptel.do_pin) != -1:
                (pin,truth) = QtGui.QInputDialog.getText(self,"Get text","Enter PIN", QtGui.QLineEdit.Normal,"Enter Pin")
                if truth:
                    response_code = self.nptel.two_step_verification(pin)
                    if response_code == 200:
                        self.msgBox.setText("Signed In Successfully")
                        self.msgBox.exec_()
                        self.nptel.load_courses()
                        self.firstScreen.remove()
                        self.LoadCoursePage()
                else:
                    self.msgBox.setText("Something Went Wrong")
                    self.msgBox.exec_()
        else:
            self.msgBox.setText("Something Went Wrong")
            self.msgBox.exec_()
        # self.firstScreen.remove()
        # self.LoadCoursePage()

    def loadCourses(self):
        i = 80
        for course in self.nptel.course_links:
            button = QtGui.QPushButton(course['Name'], self)
            button.setGeometry(QtCore.QRect(0, i, 500, 25))
            button.clicked.connect(partial(self.loadCourseContent, course))
            i += 26
            button.show()
            self.secondScreen.buttonList.append(button)
        self.update()

    def loadCourseContent(self, course):
        print "Loading Course " + course['Name']
        self.secondScreen.remove()
        self.update()
        self.splashScreen = QtGui.QSplashScreen()
        self.splashScreen.show()
        self.update()
        self.nptel.load_course_content(course)
        self.nptel.load_vid_urls()
        self.update()
        self.LoadCourseContentPage()

    def populate_course_content(self):
        i = 80
        for vid in self.nptel.videos:
            button = QtGui.QPushButton(vid['Title'], self)
            button.setGeometry(QtCore.QRect(0, i, 500, 25))
            button.clicked.connect(partial(self.download_video, vid))
            i += 26
            button.show()
            self.thirdScreen.buttonList.append(button)
        self.update()

    def download_video(self, vid):
        loading = QtGui.QPushButton("Please Wait", self)
        loading.setGeometry(QtCore.QRect(25, 50, 80, 80))
        self.update()
        self.nptel.download_vid(vid)
        loading.close()
        self.update()
        self.msgBox.setText(vid['Title'] + " Downloaded Successfully")
        self.msgBox.exec_()

    def download_all_videos(self):
        for video in self.nptel.videos:
            self.download_video(video)

    def back_to_signin(self):
        self.secondScreen.remove()
        self.LoadSignInPage()

    def back_to_coursePage(self):
        self.thirdScreen.remove()
        self.LoadCoursePage()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

run()