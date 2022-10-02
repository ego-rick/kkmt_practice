import random
import sys

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QRect, QEvent, QAbstractItemModel, QPoint, QPropertyAnimation
from PyQt5.QtGui import QBrush, QPainter, QColor, QFont, QFontMetrics, QImage, QStandardItemModel, QStandardItem, \
    QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAbstractItemView, QLayout, QStyle, QSizePolicy, \
    QGraphicsDropShadowEffect, QHBoxLayout, QCommonStyle, QScrollBar

from mdls.QNotifyWrapWind import QNotifyWrapWind
from mdls.QTableItemPracticeCard import QTableItemPracticeCard
from mdls.QWrapScrollBar import QCustomScrollBar
from res import *
from testWind import Ui_MainWindow




class QToast(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setFixedSize(10, 10)
        #self.setPosition(QPoint(self.parent().rect().x() - 30, self.parent().rect().y() - 30))

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        #self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.__initVal(parent)

    def __initVal(self, parent):
        self.__parent = parent
        self.__parent.installEventFilter(self)
        #self.installEventFilter(self)


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(QColor("red")))
        painter.setPen(QtGui.QPen(QtGui.QColor("red"), 1))
        painter.drawRect(0, 0, 10, 10)

        painter.end()

    def show(self):
        #self.raise_()
        return super().show()

    def eventFilter(self, obj, e):
        if e.type() == 14:
            self.setPosition(QPoint(0, self.parent().height() - 10))
        return super().eventFilter(obj, e)

    def setPosition(self, pos):
        geo = self.geometry()
        #geo.moveCenter(pos)
        geo.moveTo(pos)
        self.setGeometry(geo)


class QTableItem(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.text = ""
        self.pixmap = QtGui.QImage()
        #self.pixmap.fill(QtGui.qRgb(0, 0, 0))

        self.height = 60

        self.color = QColor(255, 255, 255)
        self.setFixedSize(self.parent().width(), 60)

    def setText(self, text: str):
        self.text = text

    def setImage(self, img, imgType='png'):
        imgdata = QImage.fromData(img, imgType)
        imgdata.convertToFormat(QImage.Format_ARGB32)
        #imgdata = imgdata.copy(QRect(0, 0, imgdata.width(), imgdata.height()))

        imgdata = imgdata.scaled(40, 40, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        out_img = QImage(40, 40, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)

        painter = QPainter(out_img)

        painter.setBrush(QBrush(imgdata))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 40, 40)
        painter.end()

        self.pixmap = out_img

    def paintEvent(self, event):
        self.setFixedSize(self.parent().width(), 60)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(self.color))
        painter.setPen(QtGui.QPen(self.color, 1))
        painter.drawRect(0, 0, self.parent().width(), self.height)

        painter.setBrush(QBrush(QColor(220, 225, 230)))
        painter.setPen(QtGui.QPen(QColor(220, 225, 230), 1))
        painter.drawRect(0, self.height, self.parent().width(), self.height)

        painter.drawImage(QRect(10, 10, 40, 40), self.pixmap)

        painter.setFont(QFont('Arial', 8, QFont.Bold))
        painter.setPen(QColor(26, 34, 47))
        painter.drawText(QRect(60, 9, self.parent().width() - 60, 42), Qt.TextWordWrap, self.text)
        painter.end()

    def leaveEvent(self, event):
        self.color = QColor(255, 255, 255)
        self.update()

    def enterEvent(self, event):
        self.color = QColor(245, 246, 248)
        self.update()


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


class QCardWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.parent = parent

        self.size = 302
        self.height = 167
        # self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.name = None
        self.surname = None
        self.patronymic = None
        self.group = None
        self.supervisor = None
        self.organization = None

        self.borderColor = QColor(234, 234, 234)
        self.setFixedSize(self.size, self.height)
        #self.__setShadow(QtGui.QColor(0, 0, 0, 50))

    def setData(self, values: list = ["Фамилия", "Имя", "Отчество", "Группа", "Руководитель", "Организация"]):
        self.name = values[0]
        self.surname = values[1]
        self.patronymic = values[2]
        self.group = values[3]
        self.supervisor = values[4]
        self.organization = values[5]

    def paintEvent(self, event):
        countPage = (self.parent.width() - 20 - 40) // 322
        value = ((self.parent.width() - 20 - 40) - countPage * 322) // countPage
        print((self.parent.width() - 20 - 40), self.width(), value, countPage)


        self.setFixedSize(self.size + value, self.height)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        brushMain = QBrush(QColor(255, 255, 255))
        brushLine = QBrush(QColor(224, 228, 231))

        painter.setBrush(brushMain)
        painter.setPen(QtGui.QPen(self.borderColor, 1))  # цвет пера - границы
        painter.drawRoundedRect(1, 1, self.size + value - 2, self.height - 2, 10.0, 10.0)

        painter.setBrush(brushLine)
        painter.setPen(QtGui.QPen(QColor(224, 228, 231), 2))  # цвет пера - границы

        painter.drawLine(22, 86, self.size - 22 + value, 85)

        painter.setPen(QColor(26, 34, 47))
        painter.setFont(QFont('Arial', 11, QFont.Bold))
        painter.drawText(QRect(21, 21, 100, 60), Qt.TextWordWrap, f"{self.name}\n{self.surname}\n{self.patronymic}")

        fm = QFontMetrics(QFont('Arial', 11))
        painter.setFont(QFont('Arial', 11))

        painter.setPen(QColor(146, 153, 159))
        painter.drawText(QRect(self.size - 20 - fm.width(self.group) + 1 + value, 21, 100, 60), Qt.TextWordWrap, self.group)

        painter.setFont(QFont('Arial', 10))
        painter.drawText(QRect(21, 96, self.size - 40, 20), Qt.TextWordWrap, f"     {self.supervisor}")

        painter.drawImage(QRect(21, 97, 14, 14), QImage(":/icons/icon_2.png"), QRect(0, 0, 14, 14))
        painter.drawImage(QRect(21, 117, 14, 14), QImage(":/icons/icon_1.png"), QRect(0, 0, 14, 14))

        painter.setFont(QFont('Arial', 10))
        painter.drawText(QRect(21, 116, self.size - 40, 35), Qt.TextWordWrap, f"     {self.organization}")

        painter.end()

    def enterEvent(self, event):
        self.borderColor = QColor(0, 104, 255)
        self.update()

    def leaveEvent(self, event):
        self.borderColor = QColor(234, 234, 234)
        self.update()

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
        for i in range(1, 10):
            wdgt = QCardWidget(self.scrollAreaWidgetContents)
            wdgt.setData()
            self.layoutF.addWidget(wdgt)

        name = ["CТУДЕНТЫ", "РУКОВОДИТЕЛИ", "ПРАКТИКИ", "ОРГАНИЗАЦИИ"]
        for i in name:
            wdgt = QMenuButton(self.frameBarTop)
            wdgt.setText(i)
            wdgt.setValue(random.randint(0, 1000))
            self.horizontalLayout_3.addWidget(wdgt)"""



        """self.notifBubble = QNotificationBubble(self.pushButtonNotification)
        self.notifBubble.setValue(100)"""



        image = open("./photo_organization.png", "rb").read()

        name1 = [
            'Мамонтов Корнелий Артемович',
            'Никифоров Аполлон Христофорович',
            'Карпов Корней Никитевич',
            'Анисимов Андрей Мэлорович',
            'Устинов Власий Тихонович',
            'Романов Казимир Матвеевич',
            'Филатов Лазарь Леонидович',
            'Афанасьев Мстислав Геннадиевич',
            'Федосеев Аполлон Ярославович',
            'Гаврилов Казимир Николаевич',
            'Селиверстов Бенедикт Лаврентьевич',
            'Блохин Аввакум Дмитрьевич',
            'Лобанов Геннадий Максович',
            'Панов Абрам Пётрович',
            'Попов Артур Оскарович',
            'Петухов Гарри Арсеньевич',
            'Журавлёв Юстин Тимофеевич',
            'Яковлев Афанасий Тимурович',
            'Сорокин Михаил Олегович',
            'Щербаков Андрей Романович'
        ]
        name2 = [
            'Трофимова Святослава Георгьевна',
            'Ермакова Диодора Кимовна',
            'Третьякова Хельга Пётровна',
            'Кудряшова Гражина Демьяновна'
        ]
        group = [
            'П2-19',
            'БГ20',
            'БТС1-20',
            'Ю2-20',
            'П1-20',
            'П1-19'
        ]
        date = [
            ['19.08.2022', '09.12.2022'],
            ['01.10.2022', '09.12.2022'],
            ['01.09.2022', '05.10.2022'],
            ['04.12.2022', '29.12.2022'],
            ['17.02.2022', '23.03.2022']
        ]

        org = [
            'ООО "Нерюнгринское Угледобывающее Предприятие"',
            'ОАО "Рязанский Цемент"',
            'АО "Поляны"',
            'ООО "ФИНР"',
            'ООО "ГКР"',
            'АО "Разрез Тугнуйский"',
            'ПАО "Южный Кузбасс"',
            'ООО "Суэк-Хакасия"',
            'ООО "Котен"',
            'ООО «Разрез Верхнетешский»',
            'ООО "Элси Майнинг Восток"',
            'ООО "Промпереработка"',
            'АО "УК "Кузбассразрезуголь"',
            'ООО "Шахта Байкаимская"',
            'АО "Суэк-Красноярск"',
            'АО "Донуголь"',
            'ООО "Бирауголь"',
            'ООО "ХУР"'
        ]

        """for i in org[:5]:
            wdgt = QTableItem(self.ListOwerviewScrollAreaMain)
            wdgt.setImage(image)
            wdgt.setText(i)
            self.verticalLayout_8.addWidget(wdgt)"""

        for _ in range(10):
            wdgt = QTableItemPracticeCard(self.ListOwerviewScrollAreaMain)
            wdgt.setData(
                name=name1[random.randint(0, len(name1) - 1)],
                group=group[random.randint(0, len(group) - 1)],
                curator=name2[random.randint(0, len(name2) - 1)],
                interval=date[random.randint(0, len(date) - 1)],
                semester=random.randint(3, 7)
            )
            self.verticalLayout_8.addWidget(wdgt)

        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem12)

        self.ListOwerviewScrollAreaMain.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.vsb = QCustomScrollBar(
            self.ListOwerviewScrollAreaMain,
            parentScrollBar=self.ListOwerviewScrollAreaMain.verticalScrollBar()
        )



        self.toast = QNotifyWrapWind(self.centralwidget)
        self.leftMenuButtonNotifications.clicked.connect(self.toast.toggle)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
