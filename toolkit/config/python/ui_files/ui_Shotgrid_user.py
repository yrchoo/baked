# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Shotgrid_userRIpcMY.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(350, 519)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QSize(16777215, 16777215))
        Form.setStyleSheet(u"background-color: rgb(238, 238, 236);")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.verticalLayout_3 = QVBoxLayout(self.page_1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.page_1)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Noto Sans CJK SC"])
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(self.page_1)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_6 = QLabel(self.page_1)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 27))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans CJK JP"])
        self.label_6.setFont(font1)
        self.label_6.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_8.addWidget(self.label_6)

        self.comboBox_user = QComboBox(self.page_1)
        self.comboBox_user.setObjectName(u"comboBox_user")
        sizePolicy1.setHeightForWidth(self.comboBox_user.sizePolicy().hasHeightForWidth())
        self.comboBox_user.setSizePolicy(sizePolicy1)
        self.comboBox_user.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_8.addWidget(self.comboBox_user)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.line_4 = QFrame(self.page_1)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.page_1)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(0, 27))
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_name = QLabel(self.page_1)
        self.label_name.setObjectName(u"label_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.label_name)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_ = QLabel(self.page_1)
        self.label_.setObjectName(u"label_")
        sizePolicy1.setHeightForWidth(self.label_.sizePolicy().hasHeightForWidth())
        self.label_.setSizePolicy(sizePolicy1)
        self.label_.setMinimumSize(QSize(0, 27))
        self.label_.setFont(font1)
        self.label_.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_4.addWidget(self.label_)

        self.label_email = QLabel(self.page_1)
        self.label_email.setObjectName(u"label_email")
        sizePolicy2.setHeightForWidth(self.label_email.sizePolicy().hasHeightForWidth())
        self.label_email.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.label_email)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.page_1)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(0, 27))
        self.label_4.setFont(font1)
        self.label_4.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.label_project = QLabel(self.page_1)
        self.label_project.setObjectName(u"label_project")
        sizePolicy2.setHeightForWidth(self.label_project.sizePolicy().hasHeightForWidth())
        self.label_project.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.label_project)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(self.page_1)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setMinimumSize(QSize(0, 27))
        self.label_3.setFont(font1)
        self.label_3.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_7.addWidget(self.label_3)

        self.lineEdit_task = QLineEdit(self.page_1)
        self.lineEdit_task.setObjectName(u"lineEdit_task")
        self.lineEdit_task.setStyleSheet(u"")
        self.lineEdit_task.setFrame(False)
        self.lineEdit_task.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.lineEdit_task)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_shot_asset = QLabel(self.page_1)
        self.label_shot_asset.setObjectName(u"label_shot_asset")
        sizePolicy1.setHeightForWidth(self.label_shot_asset.sizePolicy().hasHeightForWidth())
        self.label_shot_asset.setSizePolicy(sizePolicy1)
        self.label_shot_asset.setMinimumSize(QSize(0, 27))
        self.label_shot_asset.setFont(font1)
        self.label_shot_asset.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_11.addWidget(self.label_shot_asset)

        self.comboBox_shot_asset = QComboBox(self.page_1)
        self.comboBox_shot_asset.setObjectName(u"comboBox_shot_asset")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBox_shot_asset.sizePolicy().hasHeightForWidth())
        self.comboBox_shot_asset.setSizePolicy(sizePolicy4)
        self.comboBox_shot_asset.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_11.addWidget(self.comboBox_shot_asset)

        self.label_asset_type = QLabel(self.page_1)
        self.label_asset_type.setObjectName(u"label_asset_type")
        sizePolicy2.setHeightForWidth(self.label_asset_type.sizePolicy().hasHeightForWidth())
        self.label_asset_type.setSizePolicy(sizePolicy2)

        self.horizontalLayout_11.addWidget(self.label_asset_type)

        self.horizontalSpacer_4 = QSpacerItem(300, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.line_3 = QFrame(self.page_1)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.label_opennote = QLabel(self.page_1)
        self.label_opennote.setObjectName(u"label_opennote")
        sizePolicy2.setHeightForWidth(self.label_opennote.sizePolicy().hasHeightForWidth())
        self.label_opennote.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setFamilies([u"Noto Sans KR Bold"])
        font2.setPointSize(9)
        font2.setBold(True)
        self.label_opennote.setFont(font2)
        self.label_opennote.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.label_opennote)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.listWidget_note_subject = QListWidget(self.page_1)
        self.listWidget_note_subject.setObjectName(u"listWidget_note_subject")
        sizePolicy4.setHeightForWidth(self.listWidget_note_subject.sizePolicy().hasHeightForWidth())
        self.listWidget_note_subject.setSizePolicy(sizePolicy4)
        self.listWidget_note_subject.setMinimumSize(QSize(150, 50))
        self.listWidget_note_subject.setMaximumSize(QSize(150, 50))

        self.horizontalLayout_9.addWidget(self.listWidget_note_subject)

        self.plainTextEdit_note_content = QPlainTextEdit(self.page_1)
        self.plainTextEdit_note_content.setObjectName(u"plainTextEdit_note_content")
        sizePolicy4.setHeightForWidth(self.plainTextEdit_note_content.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_note_content.setSizePolicy(sizePolicy4)
        self.plainTextEdit_note_content.setMinimumSize(QSize(150, 50))
        self.plainTextEdit_note_content.setMaximumSize(QSize(150, 50))
        self.plainTextEdit_note_content.setReadOnly(True)

        self.horizontalLayout_9.addWidget(self.plainTextEdit_note_content)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.line = QFrame(self.page_1)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_add = QPushButton(self.page_1)
        self.pushButton_add.setObjectName(u"pushButton_add")
        sizePolicy1.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy1)
        self.pushButton_add.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_6.addWidget(self.pushButton_add)

        self.horizontalSpacer_6 = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.pushButton_login = QPushButton(self.page_1)
        self.pushButton_login.setObjectName(u"pushButton_login")
        sizePolicy1.setHeightForWidth(self.pushButton_login.sizePolicy().hasHeightForWidth())
        self.pushButton_login.setSizePolicy(sizePolicy1)
        self.pushButton_login.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_6.addWidget(self.pushButton_login)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_4 = QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Baked_Project", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"User :", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Name : ", None))
        self.label_name.setText("")
        self.label_.setText(QCoreApplication.translate("Form", u"Email : ", None))
        self.label_email.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"Project : ", None))
        self.label_project.setText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"Task :", None))
        self.label_shot_asset.setText(QCoreApplication.translate("Form", u"Shot/Asset :", None))
        self.label_asset_type.setText("")
        self.label_opennote.setText(QCoreApplication.translate("Form", u"OpenNote", None))
        self.pushButton_add.setText(QCoreApplication.translate("Form", u"Add User", None))
        self.pushButton_login.setText(QCoreApplication.translate("Form", u"Login", None))
    # retranslateUi

