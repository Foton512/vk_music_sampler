# -*- coding: utf-8 -*-

from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import QUrl
from captcha_dialog import CaptchaDialog

class BrowserOwner(object):
    def __init__(self, vkRequestProcessor):
        self.vkRequestProcessor = vkRequestProcessor
        self.vkRequestProcessor.openUrl.connect(self.openUrl)
        self.vkRequestProcessor.hideBrowser.connect(self.hideBrowser)
        self.vkRequestProcessor.captchaNeeded.connect(self.showCaptcha)
        self.browser = QWebView()
        self.browser.urlChanged.connect(self.urlChanged)

    def openUrl(self, url):
        self.browser.load(QUrl(url))
        self.browser.show()

    def showCaptcha(self, url):
        captchaDialog = CaptchaDialog(self, url, self.captchaTyped)
        captchaDialog.captchaTyped.connect(self.captchaTyped)
        captchaDialog.exec_()

    def hideBrowser(self):
        self.browser.hide()

    def urlChanged(self, url):
        self.vkRequestProcessor.urlChanged(url)

    def captchaTyped(self, captchaText):
        self.vkRequestProcessor.setCaptchaText(unicode(captchaText))
