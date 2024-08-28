# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Shotgrid_total_profilegGQqjP.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(488, 449)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Noto Sans CJK KR"])
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableWidget = QTableWidget(Form)
        self.tableWidget.setObjectName(u"tableWidget")

        self.horizontalLayout.addWidget(self.tableWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        font1 = QFont()
        font1.setFamilies([u"Noto Sans CJK JP"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_6.setFont(font1)

        self.verticalLayout.addWidget(self.label_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 1, -1, -1)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_name = QLineEdit(Form)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        self.lineEdit_name.setStyleSheet(u"background-color: rgb(186, 189, 182);")
        self.lineEdit_name.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit_name)

        self.horizontalSpacer = QSpacerItem(350, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 1, -1, -1)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.comboBox_task = QComboBox(Form)
        self.comboBox_task.setObjectName(u"comboBox_task")
        self.comboBox_task.setStyleSheet(u"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_3.addWidget(self.comboBox_task)

        self.horizontalSpacer_2 = QSpacerItem(300, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 1, -1, -1)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.comboBox_shot = QComboBox(Form)
        self.comboBox_shot.setObjectName(u"comboBox_shot")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_shot.sizePolicy().hasHeightForWidth())
        self.comboBox_shot.setSizePolicy(sizePolicy1)
        self.comboBox_shot.setStyleSheet(u"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_4.addWidget(self.comboBox_shot)

        self.horizontalSpacer_3 = QSpacerItem(270, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 1, -1, -1)
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.comboBox_asset = QComboBox(Form)
        self.comboBox_asset.setObjectName(u"comboBox_asset")
        self.comboBox_asset.setStyleSheet(u"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_5.addWidget(self.comboBox_asset)

        self.horizontalSpacer_4 = QSpacerItem(280, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.pushButton_insert = QPushButton(Form)
        self.pushButton_insert.setObjectName(u"pushButton_insert")
        self.pushButton_insert.setStyleSheet(u"color: rgb(46, 52, 54);\n"
"background-color: rgb(186, 189, 182);")

        self.horizontalLayout_6.addWidget(self.pushButton_insert)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setStyleSheet(QCoreApplication.translate("Form", u"color: rgb(46, 52, 54);", None))
        self.label.setText(QCoreApplication.translate("Form", u"User Profile", None))
        self.label_6.setStyleSheet(QCoreApplication.translate("Form", u"color: rgb(46, 52, 54);", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Assign Task", None))
        self.label_2.setStyleSheet(QCoreApplication.translate("Form", u"color: rgb(46, 52, 54);", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Name :", None))
        self.label_3.setStyleSheet(QCoreApplication.translate("Form", u"color: rgb(46, 52, 54);", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Task :", None))
        self.label_4.setStyleSheet(QCoreApplication.translate("Form", u"color: rgb(46, 52, 54);", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Shot :", None))
        self.label_5.setStyleSheet(QCoreApplication.translate("Form", u"color: rgb(46, 52, 54);", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Asset :", None))
        self.pushButton_insert.setText(QCoreApplication.translate("Form", u"Insert", None))
    # retranslateUi

