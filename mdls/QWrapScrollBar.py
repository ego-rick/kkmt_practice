from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class QCustomScrollBar(QtWidgets.QScrollBar):
    def __init__(self, parent=None, orientation=Qt.Vertical, parentScrollBar=None):
        QWidget.__init__(self, parent=parent)
        self.__initVal(parentScrollBar)
        self.setOrientation(orientation)

        if parentScrollBar is not None:
            parentScrollBar.valueChanged.connect(self.setValue)
            self.valueChanged.connect(parentScrollBar.setValue)
            parentScrollBar.rangeChanged.connect(self.setRange)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__out)
        self.__animation(1.0, 0.0, 1)

    def __initVal(self, parentScrollBar):
            self.parent().installEventFilter(self)
            parentScrollBar.installEventFilter(self)

    def __animation(self, startValue, endValue, duration):
        opacity_animation = QtCore.QPropertyAnimation(
            self.opacity_effect,
            b"opacity",
            duration=duration,
            startValue=startValue,
            endValue=endValue
        )

        group = QtCore.QParallelAnimationGroup(self)
        group.addAnimation(opacity_animation)
        group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    def __out(self):
        self.__animation(1.0, 0.0, 300)
        self.timer.stop()

    def leaveEvent(self, event):
        self.__animation(1.0, 0.0, 300)

    def enterEvent(self, event):
        self.__animation(0.0, 1.0, 300)

    def eventFilter(self, object, event):
        if event.type() == 14:
            self.setGeometry(self.parent().width() - 8 - 6, 0, 8 + 6, self.parent().height())
        if event.type() == 31:
            if not self.timer.isActive():
                self.__animation(0.0, 1.0, 300)
            self.timer.start(500)
        return super().eventFilter(object, event)

