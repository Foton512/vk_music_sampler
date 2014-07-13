#!/usr/bin/env python

# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from main_window import MainWindow
from vk_request_processor import VkRequestProcessor
from model import Model

def main():
    app = QApplication([])

    vkRequestProcessor = VkRequestProcessor()
    model = Model(vkRequestProcessor)
    main = MainWindow(model)
    main.show()

    app.exec_()


if __name__ == "__main__":
    main()
