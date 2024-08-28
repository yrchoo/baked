# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginOTogbq.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(308, 276)
        Form.setStyleSheet(u"background-color: rgb(238, 238, 236);")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Open Sans ExtraBold"])
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(46, 52, 54);")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Noto Sans CJK HK"])
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_name = QLineEdit(Form)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy1)
        self.lineEdit_name.setStyleSheet(u"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_2.addWidget(self.lineEdit_name)

        self.horizontalSpacer = QSpacerItem(220, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_task = QLineEdit(Form)
        self.lineEdit_task.setObjectName(u"lineEdit_task")
        self.lineEdit_task.setStyleSheet(u"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_4.addWidget(self.lineEdit_task)

        self.horizontalSpacer_3 = QSpacerItem(220, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.lineEdit_shot = QLineEdit(Form)
        self.lineEdit_shot.setObjectName(u"lineEdit_shot")
        self.lineEdit_shot.setStyleSheet(u"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_5.addWidget(self.lineEdit_shot)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.lineEdit_asset = QLineEdit(Form)
        self.lineEdit_asset.setObjectName(u"lineEdit_asset")
        self.lineEdit_asset.setStyleSheet(u"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_6.addWidget(self.lineEdit_asset)

        self.horizontalSpacer_6 = QSpacerItem(150, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.pushButton_enter = QPushButton(Form)
        self.pushButton_enter.setObjectName(u"pushButton_enter")
        self.pushButton_enter.setStyleSheet(u"color: rgb(46, 52, 54);\n"
"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_7.addWidget(self.pushButton_enter)


        self.verticalLayout.addLayout(self.horizontalLayout_7)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Log In", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Name :", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Task :", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Shot :", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Asset :", None))
        self.pushButton_enter.setText(QCoreApplication.translate("Form", u"ENTER", None))
    # retranslateUi

