# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import Qt, QUrl, pyqtSignal, QString

class CaptchaDialog(QDialog):
    captchaTyped = pyqtSignal(QString)

    def __init__(self, parent, url, callback):
        QDialog.__init__(self, parent)
        self.callback = callback

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        browser = QWebView()
        browser.load(QUrl(url))
        browser.setMinimumWidth(130)
        browser.setMaximumWidth(130)
        browser.setMinimumHeight(50)
        browser.setMaximumHeight(50)
        layout.addWidget(browser)
        self.captchaEdit = QLineEdit()
        layout.addWidget(self.captchaEdit)
        okButton = QPushButton(u"OK")
        okButton.clicked.connect(self.signalAndClose)
        layout.addWidget(okButton)

        self.setLayout(layout)

        self.setMaximumWidth(0)
        self.setMaximumHeight(0)

    def signalAndClose(self):
        self.captchaTyped.emit(self.captchaEdit.text())
        self.close()
