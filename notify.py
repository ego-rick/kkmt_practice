# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notify.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 342)
        Form.setStyleSheet("#Form {\n"
"    color: rgb(26, 34, 47);\n"
"    font: 10pt \"Arial\";\n"
"}\n"
"\n"
"#label {\n"
"    border-radius: 0px;\n"
"    border-top-left-radius: 10px;\n"
"    border-left: 1px solid rgb(234, 234, 234);\n"
"    border-top: 1px solid rgb(234, 234, 234);\n"
"}\n"
"\n"
"#label, #pushButton {\n"
"    color: rgb(68, 123, 186);\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"#pushButton {\n"
"    border-radius: 0px;\n"
"    border-top-right-radius: 10px;\n"
"    border: 1px solid rgb(234, 234, 234);\n"
"    border-bottom: none;\n"
"\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#pushButton:hover {\n"
"    background-color: rgb(248, 249, 251);\n"
"}\n"
"\n"
"#scrollArea, #scrollAreaWidgetContents {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"#scrollArea {\n"
"    border: 1px solid rgb(234, 234, 234);\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(32, 32))
        self.pushButton.setMaximumSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 398, 306))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Уведомления"))
        self.pushButton.setText(_translate("Form", "x"))