# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtSignal
from threading import Event
from settings import *
import urllib
import json

class VkRequestProcessor(QObject):
    openUrl = pyqtSignal(str)
    hideBrowser = pyqtSignal()
    captchaNeeded = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
        self.accessToken = None
        self.callback = None
        self.expectedUrlPrefix = None
        self.expectedUrlCallback = None
        self.captchaEvent = Event()
        self.captchaText = None

    def authorize(self, callback): # Does not blocks thread. callback will be called in UI thread
        try:
            accessTokenFile = open("access_token.txt", "r")
            self.accessToken = accessTokenFile.read()
            accessTokenFile.close()
            callback()
        except:
            self.callback = callback
            self.expectedUrlPrefix = authorizedUrl
            self.expectedUrlAction = self.authorizedUrlAction
            self.openUrl.emit(authUrl)

    def sendRequest(self, urlWithoutAccessToken): # sendRequest works in the same thread
                                                  # (blocks thread and can work for a long time).
        urlMainPart = "{}&access_token={}".format(urlWithoutAccessToken, self.accessToken)
        urlCaptchaPart = ""
        while True:
            url = "{}{}".format(urlMainPart, urlCaptchaPart)
            if len(urlCaptchaPart) > 0:
                urlCaptchaPart = ""
            print url

            resStr = urllib.urlopen(url).read()
            res = json.loads(resStr)
            if "response" in res:
                return res["response"]
            elif not "error" in res:
                continue
            else:
                error = res["error"]
                if not "error_code" in error:
                    return None
                errorCode = error["error_code"]
                print "Error code: {}".format(errorCode)
                if errorCode in [1, 6, 9, 10]:
                    continue
                elif errorCode == 14:
                    captchaId = error["captcha_sid"]
                    captchaUrl = error["captcha_img"]
                    self.captchaEvent.clear()
                    self.captchaNeeded.emit(captchaUrl)
                    self.captchaEvent.wait()
                    urlCaptchaPart = "&captcha_sid={}&captcha_key={}".format(captchaId, urllib.quote_plus(self.captchaText))
                    continue
                else:
                    return None

    def setCaptchaText(self, text):
        self.captchaText = text
        self.captchaEvent.set()

    def urlChanged(self, url): # called in UI thread with BrowserOwner
        urlStr = url.toString()
        if urlStr[:len(authorizedUrl)] == self.expectedUrlPrefix:
            self.expectedUrlAction(url, urlStr)

            self.hideBrowser.emit()
            self.callback()

    def authorizedUrlAction(self, url, urlStr):
        fragment = str(url.fragment())
        fragmentParameters = [param.split("=") for param in fragment.split("&")]
        for param in fragmentParameters:
            if param[0] == "access_token":
                self.accessToken = param[1]
                accessTokenFile = open("access_token.txt", "w")
                accessTokenFile.write(self.accessToken)
                accessTokenFile.close()
                break
