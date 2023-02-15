# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'weather.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QSlider, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(987, 768)
        font = QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.RBTNVL = QVBoxLayout()
        self.RBTNVL.setSpacing(15)
        self.RBTNVL.setObjectName(u"RBTNVL")
        self.RBTNVL.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.RBTNVL.setContentsMargins(0, 15, 5, 15)
        self.styleBTN = QPushButton(self.centralwidget)
        self.styleBTN.setObjectName(u"styleBTN")
        font1 = QFont()
        font1.setPointSize(14)
        self.styleBTN.setFont(font1)

        self.RBTNVL.addWidget(self.styleBTN)

        self.shortcutBTN = QPushButton(self.centralwidget)
        self.shortcutBTN.setObjectName(u"shortcutBTN")
        self.shortcutBTN.setFont(font1)

        self.RBTNVL.addWidget(self.shortcutBTN)

        self.openBTN = QPushButton(self.centralwidget)
        self.openBTN.setObjectName(u"openBTN")
        self.openBTN.setFont(font1)

        self.RBTNVL.addWidget(self.openBTN)

        self.loadBTN = QPushButton(self.centralwidget)
        self.loadBTN.setObjectName(u"loadBTN")
        self.loadBTN.setFont(font1)

        self.RBTNVL.addWidget(self.loadBTN)

        self.saveBTN = QPushButton(self.centralwidget)
        self.saveBTN.setObjectName(u"saveBTN")
        self.saveBTN.setFont(font1)

        self.RBTNVL.addWidget(self.saveBTN)

        self.lastBTN = QPushButton(self.centralwidget)
        self.lastBTN.setObjectName(u"lastBTN")
        self.lastBTN.setFont(font1)

        self.RBTNVL.addWidget(self.lastBTN)

        self.nextBTN = QPushButton(self.centralwidget)
        self.nextBTN.setObjectName(u"nextBTN")
        self.nextBTN.setFont(font1)

        self.RBTNVL.addWidget(self.nextBTN)

        self.setLastDeepBTN = QPushButton(self.centralwidget)
        self.setLastDeepBTN.setObjectName(u"setLastDeepBTN")
        self.setLastDeepBTN.setFont(font1)

        self.RBTNVL.addWidget(self.setLastDeepBTN)

        self.yesRBTN = QRadioButton(self.centralwidget)
        self.yesRBTN.setObjectName(u"yesRBTN")
        font2 = QFont()
        font2.setPointSize(16)
        self.yesRBTN.setFont(font2)
        self.yesRBTN.setChecked(True)

        self.RBTNVL.addWidget(self.yesRBTN)

        self.noRBTN = QRadioButton(self.centralwidget)
        self.noRBTN.setObjectName(u"noRBTN")
        self.noRBTN.setFont(font2)

        self.RBTNVL.addWidget(self.noRBTN)

        self.otherRBTN = QRadioButton(self.centralwidget)
        self.otherRBTN.setObjectName(u"otherRBTN")
        self.otherRBTN.setFont(font2)
        self.otherRBTN.setLayoutDirection(Qt.LeftToRight)

        self.RBTNVL.addWidget(self.otherRBTN)

        self.visLB = QLabel(self.centralwidget)
        self.visLB.setObjectName(u"visLB")
        font3 = QFont()
        font3.setPointSize(16)
        font3.setBold(False)
        self.visLB.setFont(font3)
        self.visLB.setAlignment(Qt.AlignCenter)

        self.RBTNVL.addWidget(self.visLB)

        self.deepLE = QLineEdit(self.centralwidget)
        self.deepLE.setObjectName(u"deepLE")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deepLE.sizePolicy().hasHeightForWidth())
        self.deepLE.setSizePolicy(sizePolicy)
        self.deepLE.setMinimumSize(QSize(0, 0))
        font4 = QFont()
        font4.setPointSize(20)
        font4.setBold(True)
        self.deepLE.setFont(font4)
        self.deepLE.setAlignment(Qt.AlignCenter)

        self.RBTNVL.addWidget(self.deepLE)

        self.deepVS = QSlider(self.centralwidget)
        self.deepVS.setObjectName(u"deepVS")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.deepVS.sizePolicy().hasHeightForWidth())
        self.deepVS.setSizePolicy(sizePolicy1)
        self.deepVS.setMinimum(-1)
        self.deepVS.setMaximum(99)
        self.deepVS.setSingleStep(1)
        self.deepVS.setPageStep(1)
        self.deepVS.setOrientation(Qt.Vertical)
        self.deepVS.setTickInterval(0)

        self.RBTNVL.addWidget(self.deepVS)


        self.horizontalLayout.addLayout(self.RBTNVL)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.cloudVLL = QVBoxLayout()
        self.cloudVLL.setObjectName(u"cloudVLL")

        self.horizontalLayout_2.addLayout(self.cloudVLL)

        self.cloudVLR = QVBoxLayout()
        self.cloudVLR.setObjectName(u"cloudVLR")

        self.horizontalLayout_2.addLayout(self.cloudVLR)

        self.ACoverVL = QVBoxLayout()
        self.ACoverVL.setObjectName(u"ACoverVL")
        self.ACoverLB = QLabel(self.centralwidget)
        self.ACoverLB.setObjectName(u"ACoverLB")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ACoverLB.sizePolicy().hasHeightForWidth())
        self.ACoverLB.setSizePolicy(sizePolicy2)
        self.ACoverLB.setFont(font3)
        self.ACoverLB.setAlignment(Qt.AlignCenter)

        self.ACoverVL.addWidget(self.ACoverLB)


        self.horizontalLayout_2.addLayout(self.ACoverVL)

        self.HCoverVL = QVBoxLayout()
        self.HCoverVL.setObjectName(u"HCoverVL")
        self.HCoverLB = QLabel(self.centralwidget)
        self.HCoverLB.setObjectName(u"HCoverLB")
        sizePolicy2.setHeightForWidth(self.HCoverLB.sizePolicy().hasHeightForWidth())
        self.HCoverLB.setSizePolicy(sizePolicy2)
        self.HCoverLB.setFont(font3)
        self.HCoverLB.setAlignment(Qt.AlignCenter)

        self.HCoverVL.addWidget(self.HCoverLB)


        self.horizontalLayout_2.addLayout(self.HCoverVL)

        self.MCoverVL = QVBoxLayout()
        self.MCoverVL.setObjectName(u"MCoverVL")
        self.MCoverLB = QLabel(self.centralwidget)
        self.MCoverLB.setObjectName(u"MCoverLB")
        sizePolicy2.setHeightForWidth(self.MCoverLB.sizePolicy().hasHeightForWidth())
        self.MCoverLB.setSizePolicy(sizePolicy2)
        self.MCoverLB.setFont(font3)
        self.MCoverLB.setAlignment(Qt.AlignCenter)

        self.MCoverVL.addWidget(self.MCoverLB)


        self.horizontalLayout_2.addLayout(self.MCoverVL)

        self.LCoverVL = QVBoxLayout()
        self.LCoverVL.setObjectName(u"LCoverVL")
        self.LCoverLB = QLabel(self.centralwidget)
        self.LCoverLB.setObjectName(u"LCoverLB")
        sizePolicy2.setHeightForWidth(self.LCoverLB.sizePolicy().hasHeightForWidth())
        self.LCoverLB.setSizePolicy(sizePolicy2)
        self.LCoverLB.setFont(font3)
        self.LCoverLB.setAlignment(Qt.AlignCenter)

        self.LCoverVL.addWidget(self.LCoverLB)


        self.horizontalLayout_2.addLayout(self.LCoverVL)


        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        self.qTab = QTabWidget(self.centralwidget)
        self.qTab.setObjectName(u"qTab")
        self.qTab.setEnabled(True)
        self.qTab.setMinimumSize(QSize(0, 0))
        self.qTab.setSizeIncrement(QSize(0, 0))
        self.qTab.setFont(font2)
        self.qTab.setLayoutDirection(Qt.LeftToRight)
        self.qTab.setStyleSheet(u"")
        self.qTab.setTabPosition(QTabWidget.North)
        self.qTab.setTabShape(QTabWidget.Rounded)
        self.qTab.setTabsClosable(False)
        self.qTab.setMovable(False)
        self.cloudTab = QWidget()
        self.cloudTab.setObjectName(u"cloudTab")
        self.cloudTab.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cloudTab.sizePolicy().hasHeightForWidth())
        self.cloudTab.setSizePolicy(sizePolicy3)
        self.cloudTab.setFont(font1)
        self.cloudTab.setCursor(QCursor(Qt.ArrowCursor))
        self.cloudTab.setStyleSheet(u"")
        self.qTab.addTab(self.cloudTab, "")
        self.coverTab = QWidget()
        self.coverTab.setObjectName(u"coverTab")
        self.qTab.addTab(self.coverTab, "")
        self.deepTab = QWidget()
        self.deepTab.setObjectName(u"deepTab")
        self.qTab.addTab(self.deepTab, "")
        self.visTab = QWidget()
        self.visTab.setObjectName(u"visTab")
        self.qTab.addTab(self.visTab, "")
        self.snowTab = QWidget()
        self.snowTab.setObjectName(u"snowTab")
        self.qTab.addTab(self.snowTab, "")
        self.iceTab = QWidget()
        self.iceTab.setObjectName(u"iceTab")
        self.qTab.addTab(self.iceTab, "")
        self.frostTab = QWidget()
        self.frostTab.setObjectName(u"frostTab")
        self.qTab.addTab(self.frostTab, "")
        self.dewTab = QWidget()
        self.dewTab.setObjectName(u"dewTab")
        self.qTab.addTab(self.dewTab, "")
        self.glazeTab = QWidget()
        self.glazeTab.setObjectName(u"glazeTab")
        self.qTab.addTab(self.glazeTab, "")
        self.soriTab = QWidget()
        self.soriTab.setObjectName(u"soriTab")
        self.qTab.addTab(self.soriTab, "")

        self.horizontalLayout.addWidget(self.qTab)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.qTab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5929\u6c14\u73b0\u8c61\u6807\u6ce8", None))
        self.styleBTN.setText(QCoreApplication.translate("MainWindow", u"macOS\u98ce", None))
        self.shortcutBTN.setText(QCoreApplication.translate("MainWindow", u"0-9", None))
        self.openBTN.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5939", None))
        self.loadBTN.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6", None))
        self.saveBTN.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.lastBTN.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u4e00\u5f20", None))
        self.nextBTN.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u4e00\u5f20", None))
        self.setLastDeepBTN.setText(QCoreApplication.translate("MainWindow", u"\u540c\u4e0a", None))
        self.yesRBTN.setText(QCoreApplication.translate("MainWindow", u"\u6709", None))
        self.noRBTN.setText(QCoreApplication.translate("MainWindow", u"\u65e0", None))
        self.otherRBTN.setText(QCoreApplication.translate("MainWindow", u"\u65e0\u6548", None))
        self.visLB.setText(QCoreApplication.translate("MainWindow", u"\u80fd\u89c1\u5ea6", None))
        self.deepLE.setText(QCoreApplication.translate("MainWindow", u"-1", None))
        self.ACoverLB.setText(QCoreApplication.translate("MainWindow", u"\u603b\u4e91\u91cf", None))
        self.HCoverLB.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u4e91\u91cf", None))
        self.MCoverLB.setText(QCoreApplication.translate("MainWindow", u"\u4e2d\u4e91\u91cf", None))
        self.LCoverLB.setText(QCoreApplication.translate("MainWindow", u"\u4f4e\u4e91\u91cf", None))
        self.qTab.setTabText(self.qTab.indexOf(self.cloudTab), QCoreApplication.translate("MainWindow", u"\u4e91\u72b6", None))
        self.qTab.setTabText(self.qTab.indexOf(self.coverTab), QCoreApplication.translate("MainWindow", u"\u4e91\u91cf", None))
        self.qTab.setTabText(self.qTab.indexOf(self.deepTab), QCoreApplication.translate("MainWindow", u"\u96ea\u6df1", None))
        self.qTab.setTabText(self.qTab.indexOf(self.visTab), QCoreApplication.translate("MainWindow", u"\u80fd\u89c1\u5ea6", None))
        self.qTab.setTabText(self.qTab.indexOf(self.snowTab), QCoreApplication.translate("MainWindow", u"\u79ef\u96ea", None))
        self.qTab.setTabText(self.qTab.indexOf(self.iceTab), QCoreApplication.translate("MainWindow", u"\u7ed3\u51b0", None))
        self.qTab.setTabText(self.qTab.indexOf(self.frostTab), QCoreApplication.translate("MainWindow", u"\u971c", None))
        self.qTab.setTabText(self.qTab.indexOf(self.dewTab), QCoreApplication.translate("MainWindow", u"\u9732", None))
        self.qTab.setTabText(self.qTab.indexOf(self.glazeTab), QCoreApplication.translate("MainWindow", u"\u96e8\u51c7", None))
        self.qTab.setTabText(self.qTab.indexOf(self.soriTab), QCoreApplication.translate("MainWindow", u"\u96fe\u51c7", None))
    # retranslateUi

