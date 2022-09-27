import random
import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QRect, QEvent, QAbstractItemModel
from PyQt5.QtGui import QBrush, QPainter, QColor, QFont, QFontMetrics, QImage, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAbstractItemView, QLayout, QStyle, QSizePolicy, \
    QGraphicsDropShadowEffect
from res import *
from testWind import Ui_MainWindow


class QNotificationBubble(QtWidgets.QWidget):
    def __init__(self, parent=None, parentButton=None):
        QWidget.__init__(self, parent=parent)#, parentButton=parentButton)
        self.parent = parent
        self.parentButton = parentButton
        self.value = 0
        self.setFixedSize(14, 14)

    def setValue(self, value: int):
        self.value = value

    def paintEvent(self, event):
        pos = self.parentButton.pos()
        self.setGeometry(pos.x() + 32 - 7, pos.y() - 7, 14, 14)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brushMain = QBrush(QColor(255, 29, 49))
        painter.setBrush(brushMain)
        painter.setPen(QtGui.QPen(QColor(255, 29, 49), 1))
        painter.drawRoundedRect(0, 0, 14, 14, 10.0, 10.0)

        painter.setFont(QFont('Arial', 8, QFont.Bold))
        fm = QFontMetrics(QFont('Arial', 8, QFont.Bold))

        painter.setPen(QColor(255, 255, 255))
        painter.drawText(QRect(0, 0, 14, 14), Qt.TextWordWrap, str(self.value))

        painter.end()


class QMenuButton(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.toggle = False
        self.valueVisible = False

        self.text = ""
        self.value = 0
        self.width = 50
        self.height = 53
        self.setFixedSize(self.width, self.height)

    def __setWidth(self):
        fm = QFontMetrics(QFont('Arial', 8, QFont.Bold))
        self.width = fm.width(self.text)

        if self.valueVisible:
            self.width = self.width + fm.width(str(self.value)) + 15 + 1

        self.setFixedSize(self.width, self.height)

    def setValue(self, value: int):
        self.value = value
        self.__setWidth()

    def setText(self, text: str):
        self.text = text
        self.__setWidth()

    def disableValue(self):
        if self.valueVisible:
            self.valueVisible = False

    def enableValue(self):
        if not self.valueVisible:
            self.valueVisible = True

    def mousePressEvent(self, event):
        """if not self.toggle:
            self.toggle = True"""

        self.toggle = False if self.toggle else True
        self.update()

    def leaveEvent(self, event):
        pass

    def enterEvent(self, event):
        pass

    def paintEvent(self, event):
        if self.toggle:
            color = QtGui.QColor(0, 104, 255)
        else:
            color = QtGui.QColor(146, 153, 159)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brushMain = QBrush(QColor("white"))
        painter.setBrush(brushMain)
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 1))
        painter.drawRect(0, 0, self.width, self.height)

        painter.setFont(QFont('Arial', 8, QFont.Bold))
        fm = QFontMetrics(QFont('Arial', 8, QFont.Bold))

        painter.setPen(color)
        painter.drawText(QRect(0, self.height // 2 - 4, fm.width(self.text), 20), Qt.TextWordWrap, self.text)

        if self.valueVisible:
            if self.toggle:
                colorText = QColor(255, 255, 255)
                colorBubble = QColor(0, 104, 255)
            else:
                colorText = QColor(color)
                colorBubble = QColor(225, 228, 233)

            brushMain = QBrush(colorBubble)
            painter.setBrush(brushMain)
            painter.setPen(colorBubble)
            painter.drawRoundedRect(fm.width(self.text) + 5, self.height // 2 - 5, fm.width(str(self.value)) + 10, 16,
                                    8.0, 8.0)

            painter.setPen(colorText)
            painter.drawText(QRect(fm.width(self.text) + 10, self.height // 2 - 4, fm.width(str(self.value)), 20),
                             Qt.TextWordWrap, str(self.value))

        if self.toggle:
            brushMain = QBrush(color)
            painter.setBrush(brushMain)
            painter.setPen(color)
            painter.drawRoundedRect(0, self.height - 2, self.width, 2, 5.0, 5.0)
            painter.drawRect(0, self.height - 1, self.width, 1)

        painter.end()


class QNotification(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.parent = parent

        self.size = 300
        self.height = 165
        # self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.name = None
        self.surname = None
        self.patronymic = None
        self.group = None
        self.supervisor = None
        self.organization = None

        self.setFixedSize(self.size, self.height)
        self.__setShadow(QtGui.QColor(0, 0, 0, 50))

    def setData(self, values: list = ["Фамилия", "Имя", "Отчество", "Группа", "Руководитель", "Организация"]):
        self.name = values[0]
        self.surname = values[1]
        self.patronymic = values[2]
        self.group = values[3]
        self.supervisor = values[4]
        self.organization = values[5]

    def paintEvent(self, event):
        countPage = (self.parent.width() - 40 - 20) // 320
        value = ((self.parent.width() - 40 - 40) - countPage * 300 - (countPage - 1) * 20) // countPage - 10


        if value < 0:
            value = 0

        self.setFixedSize(self.size + value, self.height)

        painter = QPainter()
        painter.begin(self)

        brushMain = QBrush(QColor(255, 255, 255))
        brushLine = QBrush(QColor(224, 228, 231))

        painter.setBrush(brushMain)
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 1))  # цвет пера - границы
        painter.drawRoundedRect(0, 0, self.size + value, self.height, 10.0, 10.0)

        painter.setBrush(brushLine)
        painter.setPen(QtGui.QPen(QColor(224, 228, 231), 2))  # цвет пера - границы

        painter.drawLine(21, 85, self.size - 22, 85)

        painter.setPen(QColor(26, 34, 47))
        painter.setFont(QFont('Arial', 11, QFont.Bold))
        painter.drawText(QRect(20, 20, 100, 60), Qt.TextWordWrap, f"{self.name}\n{self.surname}\n{self.patronymic}")

        fm = QFontMetrics(QFont('Arial', 11))
        painter.setFont(QFont('Arial', 11))

        painter.setPen(QColor(146, 153, 159))
        painter.drawText(QRect(self.size - 20 - fm.width(self.group), 20, 100, 60), Qt.TextWordWrap, self.group)

        painter.setFont(QFont('Arial', 10))
        painter.drawText(QRect(20, 95, self.size - 40, 20), Qt.TextWordWrap, f"     {self.supervisor}")

        painter.drawImage(QRect(20, 96, 14, 14), QImage(":/icons/icon_2.png"), QRect(0, 0, 14, 14))
        painter.drawImage(QRect(20, 116, 14, 14), QImage(":/icons/icon_1.png"), QRect(0, 0, 14, 14))

        painter.setFont(QFont('Arial', 10))
        painter.drawText(QRect(20, 115, self.size - 40, 35), Qt.TextWordWrap, f"     {self.organization}")

        painter.end()

    def __setShadow(self, shadowColor):
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            self,
            blurRadius=7.0,
            color=shadowColor,
            offset=QtCore.QPointF(0, 0)
        )
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self.__setShadow(QtGui.QColor(0, 104, 255, 200))

    def leaveEvent(self, event):
        self.__setShadow(QtGui.QColor(0, 0, 0, 50))

    def mousePressEvent(self, event):
        print("Кар")


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton, Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        """self.layoutF = FlowLayout(parent=self.framePage1_second, hspacing=20, vspacing=20, margin=20)
        for i in range(1, 50):
            wdgt = QNotification(self.scrollAreaWidgetContents)
            wdgt.setData()
            self.layoutF.addWidget(wdgt)"""

        name = ["CТУДЕНТЫ", "РУКОВОДИТЕЛИ", "ПРАКТИКИ"]
        for i in name:
            wdgt = QMenuButton(self.frameBarTop)
            wdgt.setText(i)
            wdgt.setValue(random.randint(0, 1000))
            self.horizontalLayout_3.addWidget(wdgt)

        shadow = QtWidgets.QGraphicsDropShadowEffect(
            self,
            blurRadius=9.0,
            color=QColor(0, 0, 0, 50),
            offset=QtCore.QPointF(0, 0)
        )
        #self.frameBarTop.setGraphicsEffect(shadow)

        self.notifBubble = QNotificationBubble(self.pushButton, self.pushButton)
        #self.horizontalLayout_2.addWidget(self.notifBubble)
        # self.setGeometry(300, 300, 355, 280)
        # self.wdgt = QNotification(parent=self, size=300)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
