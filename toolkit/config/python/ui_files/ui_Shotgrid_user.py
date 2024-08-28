# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Shotgrid_userbEEYUx.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(533, 596)
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
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
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
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

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
        sizePolicy.setHeightForWidth(self.comboBox_user.sizePolicy().hasHeightForWidth())
        self.comboBox_user.setSizePolicy(sizePolicy)
        self.comboBox_user.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_8.addWidget(self.comboBox_user)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.page_1)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(0, 27))
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_name = QLabel(self.page_1)
        self.label_name.setObjectName(u"label_name")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_name)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_ = QLabel(self.page_1)
        self.label_.setObjectName(u"label_")
        sizePolicy.setHeightForWidth(self.label_.sizePolicy().hasHeightForWidth())
        self.label_.setSizePolicy(sizePolicy)
        self.label_.setMinimumSize(QSize(0, 27))
        self.label_.setFont(font1)
        self.label_.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_4.addWidget(self.label_)

        self.label_email = QLabel(self.page_1)
        self.label_email.setObjectName(u"label_email")
        sizePolicy1.setHeightForWidth(self.label_email.sizePolicy().hasHeightForWidth())
        self.label_email.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.label_email)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.page_1)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(0, 27))
        self.label_4.setFont(font1)
        self.label_4.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.label_project = QLabel(self.page_1)
        self.label_project.setObjectName(u"label_project")
        sizePolicy1.setHeightForWidth(self.label_project.sizePolicy().hasHeightForWidth())
        self.label_project.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.label_project)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.page_1)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(0, 27))
        self.label_5.setFont(font1)
        self.label_5.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_6.addWidget(self.label_5)

        self.label_role = QLabel(self.page_1)
        self.label_role.setObjectName(u"label_role")
        sizePolicy1.setHeightForWidth(self.label_role.sizePolicy().hasHeightForWidth())
        self.label_role.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.label_role)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(self.page_1)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
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

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_shot_asset = QLabel(self.page_1)
        self.label_shot_asset.setObjectName(u"label_shot_asset")
        sizePolicy2.setHeightForWidth(self.label_shot_asset.sizePolicy().hasHeightForWidth())
        self.label_shot_asset.setSizePolicy(sizePolicy2)
        self.label_shot_asset.setMinimumSize(QSize(0, 27))
        self.label_shot_asset.setFont(font1)
        self.label_shot_asset.setStyleSheet(u"color: rgb(46, 52, 54);")

        self.horizontalLayout_10.addWidget(self.label_shot_asset)

        self.comboBox_shot_asset = QComboBox(self.page_1)
        self.comboBox_shot_asset.setObjectName(u"comboBox_shot_asset")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_shot_asset.sizePolicy().hasHeightForWidth())
        self.comboBox_shot_asset.setSizePolicy(sizePolicy3)
        self.comboBox_shot_asset.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_10.addWidget(self.comboBox_shot_asset)

        self.label_type = QLabel(self.page_1)
        self.label_type.setObjectName(u"label_type")

        self.horizontalLayout_10.addWidget(self.label_type)

        self.label_asset_type = QLabel(self.page_1)
        self.label_asset_type.setObjectName(u"label_asset_type")

        self.horizontalLayout_10.addWidget(self.label_asset_type)

        self.horizontalSpacer_4 = QSpacerItem(300, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, -1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setSpacing(6)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_image = QLabel(self.page_1)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setMinimumSize(QSize(192, 108))
        self.label_image.setMaximumSize(QSize(192, 108))
        self.label_image.setStyleSheet(u"border-color: 3px solid blue;")
        self.label_image.setInputMethodHints(Qt.ImhNone)
        self.label_image.setFrameShape(QFrame.NoFrame)
        self.label_image.setMidLineWidth(0)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_image)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_15)

        self.line_3 = QFrame(self.page_1)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, 0, -1, -1)
        self.label_opennote = QLabel(self.page_1)
        self.label_opennote.setObjectName(u"label_opennote")
        font2 = QFont()
        font2.setFamilies([u"Noto Sans KR Bold"])
        font2.setPointSize(9)
        font2.setBold(True)
        self.label_opennote.setFont(font2)

        self.horizontalLayout_16.addWidget(self.label_opennote)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.listWidget_note_subject = QListWidget(self.page_1)
        self.listWidget_note_subject.setObjectName(u"listWidget_note_subject")

        self.horizontalLayout_11.addWidget(self.listWidget_note_subject)

        self.plainTextEdit_note_content = QPlainTextEdit(self.page_1)
        self.plainTextEdit_note_content.setObjectName(u"plainTextEdit_note_content")

        self.horizontalLayout_11.addWidget(self.plainTextEdit_note_content)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.line = QFrame(self.page_1)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.pushButton_add = QPushButton(self.page_1)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_3.addWidget(self.pushButton_add)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.pushButton_login = QPushButton(self.page_1)
        self.pushButton_login.setObjectName(u"pushButton_login")
        sizePolicy.setHeightForWidth(self.pushButton_login.sizePolicy().hasHeightForWidth())
        self.pushButton_login.setSizePolicy(sizePolicy)
        self.pushButton_login.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_3.addWidget(self.pushButton_login)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_4 = QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.label_29 = QLabel(self.page_2)
        self.label_29.setObjectName(u"label_29")
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setFamilies([u"Noto Sans CJK SC"])
        font3.setBold(True)
        font3.setItalic(False)
        self.label_29.setFont(font3)
        self.label_29.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_44.addWidget(self.label_29)


        self.verticalLayout_4.addLayout(self.horizontalLayout_44)

        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.label_30 = QLabel(self.page_2)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_45.addWidget(self.label_30)

        self.comboBox_user_4 = QComboBox(self.page_2)
        self.comboBox_user_4.setObjectName(u"comboBox_user_4")
        sizePolicy.setHeightForWidth(self.comboBox_user_4.sizePolicy().hasHeightForWidth())
        self.comboBox_user_4.setSizePolicy(sizePolicy)
        self.comboBox_user_4.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_45.addWidget(self.comboBox_user_4)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_45.addItem(self.horizontalSpacer_25)


        self.verticalLayout_4.addLayout(self.horizontalLayout_45)

        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.label_31 = QLabel(self.page_2)
        self.label_31.setObjectName(u"label_31")
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_46.addWidget(self.label_31)

        self.label_name_4 = QLabel(self.page_2)
        self.label_name_4.setObjectName(u"label_name_4")
        sizePolicy1.setHeightForWidth(self.label_name_4.sizePolicy().hasHeightForWidth())
        self.label_name_4.setSizePolicy(sizePolicy1)

        self.horizontalLayout_46.addWidget(self.label_name_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_46)

        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.label_32 = QLabel(self.page_2)
        self.label_32.setObjectName(u"label_32")
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        self.label_32.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_47.addWidget(self.label_32)

        self.label_email_4 = QLabel(self.page_2)
        self.label_email_4.setObjectName(u"label_email_4")
        sizePolicy1.setHeightForWidth(self.label_email_4.sizePolicy().hasHeightForWidth())
        self.label_email_4.setSizePolicy(sizePolicy1)

        self.horizontalLayout_47.addWidget(self.label_email_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_47)

        self.horizontalLayout_48 = QHBoxLayout()
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.label_33 = QLabel(self.page_2)
        self.label_33.setObjectName(u"label_33")
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_48.addWidget(self.label_33)

        self.label_project_4 = QLabel(self.page_2)
        self.label_project_4.setObjectName(u"label_project_4")
        sizePolicy1.setHeightForWidth(self.label_project_4.sizePolicy().hasHeightForWidth())
        self.label_project_4.setSizePolicy(sizePolicy1)

        self.horizontalLayout_48.addWidget(self.label_project_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_48)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.label_34 = QLabel(self.page_2)
        self.label_34.setObjectName(u"label_34")
        sizePolicy.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)
        self.label_34.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_49.addWidget(self.label_34)

        self.label_role_4 = QLabel(self.page_2)
        self.label_role_4.setObjectName(u"label_role_4")
        sizePolicy1.setHeightForWidth(self.label_role_4.sizePolicy().hasHeightForWidth())
        self.label_role_4.setSizePolicy(sizePolicy1)

        self.horizontalLayout_49.addWidget(self.label_role_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_49)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.label_35 = QLabel(self.page_2)
        self.label_35.setObjectName(u"label_35")
        sizePolicy2.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy2)
        self.label_35.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_50.addWidget(self.label_35)

        self.lineEdit_task_4 = QLineEdit(self.page_2)
        self.lineEdit_task_4.setObjectName(u"lineEdit_task_4")
        self.lineEdit_task_4.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")
        self.lineEdit_task_4.setReadOnly(True)

        self.horizontalLayout_50.addWidget(self.lineEdit_task_4)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_50.addItem(self.horizontalSpacer_30)


        self.verticalLayout_4.addLayout(self.horizontalLayout_50)

        self.horizontalLayout_51 = QHBoxLayout()
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.label_seq_shot_4 = QLabel(self.page_2)
        self.label_seq_shot_4.setObjectName(u"label_seq_shot_4")
        sizePolicy2.setHeightForWidth(self.label_seq_shot_4.sizePolicy().hasHeightForWidth())
        self.label_seq_shot_4.setSizePolicy(sizePolicy2)
        self.label_seq_shot_4.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_51.addWidget(self.label_seq_shot_4)

        self.comboBox_seq_4 = QComboBox(self.page_2)
        self.comboBox_seq_4.setObjectName(u"comboBox_seq_4")
        self.comboBox_seq_4.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_51.addWidget(self.comboBox_seq_4)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_31)


        self.verticalLayout_4.addLayout(self.horizontalLayout_51)

        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.label_asset_4 = QLabel(self.page_2)
        self.label_asset_4.setObjectName(u"label_asset_4")
        sizePolicy2.setHeightForWidth(self.label_asset_4.sizePolicy().hasHeightForWidth())
        self.label_asset_4.setSizePolicy(sizePolicy2)
        self.label_asset_4.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_53.addWidget(self.label_asset_4)

        self.comboBox_asset_4 = QComboBox(self.page_2)
        self.comboBox_asset_4.setObjectName(u"comboBox_asset_4")
        sizePolicy1.setHeightForWidth(self.comboBox_asset_4.sizePolicy().hasHeightForWidth())
        self.comboBox_asset_4.setSizePolicy(sizePolicy1)
        self.comboBox_asset_4.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_53.addWidget(self.comboBox_asset_4)

        self.horizontalSpacer_33 = QSpacerItem(55, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_53.addItem(self.horizontalSpacer_33)

        self.label_36 = QLabel(self.page_2)
        self.label_36.setObjectName(u"label_36")
        sizePolicy2.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy2)
        self.label_36.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_53.addWidget(self.label_36)

        self.comboBox_shot_4 = QComboBox(self.page_2)
        self.comboBox_shot_4.setObjectName(u"comboBox_shot_4")
        self.comboBox_shot_4.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_53.addWidget(self.comboBox_shot_4)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_53.addItem(self.horizontalSpacer_32)


        self.verticalLayout_4.addLayout(self.horizontalLayout_53)

        self.horizontalLayout_54 = QHBoxLayout()
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.frame = QFrame(self.page_2)
        self.frame.setObjectName(u"frame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy4)
        self.frame.setMinimumSize(QSize(150, 150))
        self.frame.setMaximumSize(QSize(150, 150))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.horizontalLayout_54.addWidget(self.frame)

        self.horizontalSpacer_34 = QSpacerItem(180, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_54.addItem(self.horizontalSpacer_34)

        self.frame_4 = QFrame(self.page_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(150, 150))
        self.frame_4.setMaximumSize(QSize(150, 150))
        self.frame_4.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_54.addWidget(self.frame_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_54)

        self.horizontalLayout_55 = QHBoxLayout()
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.horizontalLayout_55.setContentsMargins(-1, 0, -1, -1)
        self.label_37 = QLabel(self.page_2)
        self.label_37.setObjectName(u"label_37")
        sizePolicy2.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy2)
        self.label_37.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_55.addWidget(self.label_37)

        self.comboBox_asset_type_4 = QComboBox(self.page_2)
        self.comboBox_asset_type_4.setObjectName(u"comboBox_asset_type_4")
        self.comboBox_asset_type_4.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_55.addWidget(self.comboBox_asset_type_4)

        self.spacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_55.addItem(self.spacer_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_55)

        self.horizontalLayout_56 = QHBoxLayout()
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.label_38 = QLabel(self.page_2)
        self.label_38.setObjectName(u"label_38")
        sizePolicy2.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy2)
        font4 = QFont()
        font4.setFamilies([u"Noto Sans CJK SC"])
        font4.setBold(False)
        font4.setItalic(False)
        self.label_38.setFont(font4)
        self.label_38.setStyleSheet(u"color: rgb(238, 238, 236);")

        self.horizontalLayout_56.addWidget(self.label_38)

        self.pushButton_add_4 = QPushButton(self.page_2)
        self.pushButton_add_4.setObjectName(u"pushButton_add_4")
        self.pushButton_add_4.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_56.addWidget(self.pushButton_add_4)

        self.horizontalSpacer_35 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_56.addItem(self.horizontalSpacer_35)


        self.verticalLayout_4.addLayout(self.horizontalLayout_56)

        self.horizontalSpacer_36 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_4.addItem(self.horizontalSpacer_36)

        self.horizontalLayout_57 = QHBoxLayout()
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.horizontalLayout_57.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_37 = QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_57.addItem(self.horizontalSpacer_37)

        self.pushButton_login_4 = QPushButton(self.page_2)
        self.pushButton_login_4.setObjectName(u"pushButton_login_4")
        sizePolicy.setHeightForWidth(self.pushButton_login_4.sizePolicy().hasHeightForWidth())
        self.pushButton_login_4.setSizePolicy(sizePolicy)
        self.pushButton_login_4.setStyleSheet(u"background-color: rgb(186, 189, 182);\n"
"color: rgb(46, 52, 54);")

        self.horizontalLayout_57.addWidget(self.pushButton_login_4)

        self.horizontalSpacer_38 = QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_57.addItem(self.horizontalSpacer_38)


        self.verticalLayout_4.addLayout(self.horizontalLayout_57)

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
        self.label_5.setText(QCoreApplication.translate("Form", u"Role : ", None))
        self.label_role.setText("")
        self.label_3.setText(QCoreApplication.translate("Form", u"Task :", None))
        self.label_shot_asset.setText(QCoreApplication.translate("Form", u"Shot/Asset :", None))
        self.label_type.setText("")
        self.label_asset_type.setText("")
        self.label_image.setText("")
        self.label_opennote.setText(QCoreApplication.translate("Form", u"OpenNote", None))
        self.pushButton_add.setText(QCoreApplication.translate("Form", u"Add User", None))
        self.pushButton_login.setText(QCoreApplication.translate("Form", u"Login", None))
        self.label_29.setText(QCoreApplication.translate("Form", u"Baked_Project", None))
        self.label_30.setText(QCoreApplication.translate("Form", u"User :", None))
        self.label_31.setText(QCoreApplication.translate("Form", u"Name : ", None))
        self.label_name_4.setText("")
        self.label_32.setText(QCoreApplication.translate("Form", u"Email : ", None))
        self.label_email_4.setText("")
        self.label_33.setText(QCoreApplication.translate("Form", u"Project : ", None))
        self.label_project_4.setText("")
        self.label_34.setText(QCoreApplication.translate("Form", u"Role : ", None))
        self.label_role_4.setText("")
        self.label_35.setText(QCoreApplication.translate("Form", u"Task :", None))
        self.label_seq_shot_4.setText(QCoreApplication.translate("Form", u"Seq :", None))
        self.label_asset_4.setText(QCoreApplication.translate("Form", u"Shot :", None))
        self.label_36.setText(QCoreApplication.translate("Form", u"Asset :", None))
        self.label_37.setText(QCoreApplication.translate("Form", u"Asset_Type :", None))
        self.label_38.setText(QCoreApplication.translate("Form", u"Update Task :", None))
        self.pushButton_add_4.setText(QCoreApplication.translate("Form", u"Add", None))
        self.pushButton_login_4.setText(QCoreApplication.translate("Form", u"Login", None))
    # retranslateUi

