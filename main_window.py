# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from browser_owner import BrowserOwner
from settings import *

class MainWindow(QMainWindow, BrowserOwner):
    def __init__(self, model):
        QMainWindow.__init__(self)
        BrowserOwner.__init__(self, model.getVkRequestProcessor())
        self.model = model
        self.model.infoReady.connect(self.showInfo)
        self.vkRequestProcessor = model.getVkRequestProcessor()
        self.initUI()

    def initUI(self):
        self.setGeometry(windowLeft, windowTop, windowWidth, windowHeight)
        self.setWindowTitle(u"VK Music Sampler")    

        mainWidget = QWidget()
        mainLayout = QVBoxLayout()

        nUsersLayout = QHBoxLayout()
        nUsersLayout.setContentsMargins(0, 0, 0, 0)
        nUsersLayout.setAlignment(Qt.AlignLeft)
        nUsersLayout.addWidget(QLabel("Number of users"))
        self.nUsersEdit = QLineEdit("100")
        self.nUsersEdit.setMinimumWidth(100)
        self.nUsersEdit.setMaximumWidth(100)
        nUsersLayout.addWidget(self.nUsersEdit)
        nUsersLayout.addItem(QSpacerItem(0, 0, hPolicy = QSizePolicy.Expanding))
        nUsersWidget = QWidget()
        nUsersWidget.setLayout(nUsersLayout)
        mainLayout.addWidget(nUsersWidget)

        sampleSizeLayout = QHBoxLayout()
        sampleSizeLayout.setContentsMargins(0, 0, 0, 0)
        sampleSizeLayout.setAlignment(Qt.AlignLeft)
        sampleSizeLayout.addWidget(QLabel("Maximum sample size"))
        self.sampleSizeEdit = QLineEdit("1000000")
        self.sampleSizeEdit.setMinimumWidth(100)
        self.sampleSizeEdit.setMaximumWidth(100)
        sampleSizeLayout.addWidget(self.sampleSizeEdit)
        sampleSizeLayout.addItem(QSpacerItem(0, 0, hPolicy = QSizePolicy.Expanding))
        sampleSizeWidget = QWidget()
        sampleSizeWidget.setLayout(sampleSizeLayout)
        mainLayout.addWidget(sampleSizeWidget)

        authButton = QPushButton(u"Prepare sample")
        authButton.clicked.connect(self.authButtonClicked)
        mainLayout.addWidget(authButton)
        self.textEdit = QTextEdit()
        mainLayout.addWidget(self.textEdit)
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        self.show()

    def authButtonClicked(self):
        self.model.setNUsers(self.nUsersEdit.text().toInt()[0])
        self.model.setSampleSize(self.sampleSizeEdit.text().toInt()[0])
        self.vkRequestProcessor.authorize(self.authorized)

    def authorized(self):
        self.model.setAccessToken(self.vkRequestProcessor.accessToken)
        self.model.prepareSampleAsync()
        
    def showInfo(self, infoStr):
        self.textEdit.setText(infoStr)
