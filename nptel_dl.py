__author__ = 'Pranay'

import mechanize
import youtube_dl
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from PyQt4 import QtCore
from subprocess import check_output


class NPTEL_DL(QtCore.QThread):
    def __init__(self):
        self.br = mechanize.Browser()
        try:
            self.open_browser()
        except WindowsError:
            self.open_browser()
        self.driver.set_window_size(0, 0, windowHandle='current')
        self.base_url = "https://onlinecourses.nptel.ac.in"
        sign_in_url = "https://accounts.google.com/ServiceLogin?service=ah&passive=true&continue=https%3A%2F%2Fappengine.google.com%2F_ah%2Fconflogin%3Fcontinue%3Dhttps%3A%2F%2Fonlinecourses.nptel.ac.in%2F&ltmpl=gm&shdf=CiALEgZhaG5hbWUaFE5QVEVMIE9ubGluZSBDb3Vyc2VzDBICYWgiFA32zMXt69d67Y99rnDmYcdWzpWJKAEyFCgKypfwnKXxFvvoPY85CyUnV2OE#identifier"
        self.do_pin = "accounts.google.com"
        self.course_links = []
        self.contents = []
        self.videos = []
        self.open_signinpage(sign_in_url)
        self.function = None

    def run(self):
        self.function()

    def open_browser(self):
        self.driver = webdriver.Firefox()

    def open_signinpage(self, sign_in_url):
        self.br.set_handle_robots(False)
        self.response = self.br.open(sign_in_url)
        print(self.response.code)
        return self.response.code

    def sign_in(self, Email, Passwd):
        self.br.select_form(nr=0)
        self.br.form["Email"] = Email
        self.br.form["Passwd"] = Passwd
        re = self.br.submit()
        print(self.response.code)
        return re.code, self.br.geturl()

    def two_step_verification(self, pin):
         self.br.select_form(nr=0)
         self.br.form["Pin"] = pin
         self.br.find_control("TrustDevice").items[0].selected=False
         re = self.br.submit()
         print(self.response.code)
         if re.code == 200:
             return self.conform_google_accnt()
         return re.code

    def conform_google_accnt(self):
        try:
            self.br.select_form(nr=0)
        except mechanize._form.ParseError:
            print "Something went worng while siging in.\nPlease try manual sign in and try again"
        self.br.form["authuser"] = 0
        self.br.find_control("persist").items[0].selected=False
        re = self.br.submit(nr=0)
        return re.code

    def load_courses(self):
        profile_link = "/explorer/profile"
        for link in self.br.links():
            if link.url == profile_link:
                break
        link.absolute_url = mechanize.urljoin(self.base_url, link.url)
        self.br.follow_link(link)
        # Scrapping urls to user's courses
        profilePage = BeautifulSoup(self.br.response().read(), 'html.parser')
        course_tags = profilePage.find_all('th', {'class':'gcb-align-left'})
        links_dict = {}
        for links in self.br.links():
            if links.text != None:
                links_dict[(links.text).strip()] = links
        for course in course_tags[2:]:
            dict = {}
            link_tag = course.find('a')
            key = (link_tag.text).strip()
            dict['Name'] = key
            dict['URL'] = links_dict[key]
            dict['URL'].absolute_url = mechanize.urljoin(self.base_url, dict['URL'].url)
            self.course_links.append(dict)


    def print_courses(self):
        i = 1
        print '--------------------------------------------------------------------------------------------------------------------\n'
        print 'Your Courses\n'
        for course in self.course_links:
            print str(i)+ " " + course['Name'] + " - " + course['URL'].absolute_url
            i+=1

    def load_course_content(self, course):
        self.br.follow_link(course['URL'])
        print course['Name'] + '\n'
        content_links = {}
        for link in self.br.links():
            if link.text != None and link.url != None:
                content_links[link.text] = link
        course_page = BeautifulSoup(self.br.response().read(), 'html.parser')
        content_tag = course_page.find_all('div', {'class':'gcb-left-activity-title-with-progress'})
        for content in content_tag:
            dict = {}
            link_tag = content.find('a')
            key = (link_tag.text).strip()
            try:
                dict['Name'] = key
                dict['URL'] =  content_links[key]
                self.contents.append(dict)
            except KeyError:
                print "URL text contains some special character"
                print key + " Not added in the downloading list. Download it manually"

    def load_vid_urls(self):
        i = 1
        for content in self.contents[0:]:
            self.br.follow_link(content['URL'])
            f = open('page.html','w')
            f.write(self.br.response().read())
            s = os.path.abspath('page.html')
            s.replace('\\', '/')
            self.br.back()
            self.driver.get("file:///" + s)
            dict = {}
            try:
                vidElement = self.driver.find_element_by_id("videoDiv")
                titleElement = self.driver.find_element_by_class_name("gcb-lesson-title")
                vidUrl = vidElement.get_attribute('src')
                vidTitle = titleElement.text
                dict['Title'] = vidTitle.strip()
                dict['URL'] = vidUrl
                self.videos.append(dict)
                i += 1
            except Exception:
                pass
        self.driver.close()

    def print_vid_urls(self):
        i = 1
        for vid in self.videos:
            print str(i) + ". " + vid['Title'] + " - " + vid['URL']
            i += 1

    def download_vid(self, vid):
        # ydl_opts = {}
        # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #     print '\nDownloading '+vid['Title']
        #     ydl.download([vid['URL']])
        check_output("youtube-dl "+vid['URL'], shell=True)