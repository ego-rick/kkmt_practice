from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class QNotifyWrapWind(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)

        self.height = 400
        self.width = 300
        self.__initVal()

        self.setFixedSize(self.width, self.height)

        self.setStyleSheet("QWidget {\n"
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
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self)
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
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 398, 306))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.animate = QtCore.QPropertyAnimation(self, b'pos', self)
        self.animate.setDuration(100)
        self.animate.finished.connect(self.__visibility)
        self.pushButton.clicked.connect(self.toggle)
        self.toggleWrap = False
        self.hide()
        shadow = QtWidgets.QGraphicsDropShadowEffect(self,
             blurRadius=80.0,
             color=QtGui.QColor(0, 0, 0, 100),
             offset=QtCore.QPointF(0.0, 0.0)
             )
        self.setGraphicsEffect(shadow)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Уведомления"))
        self.pushButton.setText(_translate("Form", "x"))

    def toggle(self):
        self.__animation()

    def __visibility(self):
        if self.toggleWrap:
            self.toggleWrap = False
            self.hide()
        else:
            self.toggleWrap = True

    def __animation(self):
        if self.toggleWrap:
            pos_1 = self.pos()
            pos_2 = self.parent().height()
        else:
            pos_1 = QtCore.QPoint(0, self.parent().height())
            pos_2 = self.parent().height() - self.height

        self.animate.setStartValue(pos_1)
        self.animate.setEndValue(QtCore.QPoint(0, pos_2))

        if not self.toggleWrap:
            self.show()

        self.animate.start()






    def __initVal(self):
        self.parent().installEventFilter(self)
        #self.installEventFilter(self)

    """def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        #painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QtGui.QPen(QtGui.QColor(234, 234, 234), 1))
        painter.drawRoundedRect(QRect(0, 0, self.width - 1, self.height), 20.0, 15.0)

        painter.end()"""

    def show(self):
        return super().show()

    def eventFilter(self, obj, e):
        if self.toggleWrap and e.type() == 14:
            self.setPosition(QPoint(0, self.parent().height() - self.height))
        return super().eventFilter(obj, e)

    def setPosition(self, pos):
        geo = self.geometry()
        #geo.moveCenter(pos)
        geo.moveTo(pos)
        self.setGeometry(geo)