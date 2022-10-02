from math import cos, pi, sin

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QFontMetrics, QFont, QImage
from PyQt5.QtWidgets import QWidget

from datetime import datetime, timedelta


class QTableItemPracticeCard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.name = None
        self.group = None
        self.semester = None
        self.curator = None
        self.interval = None

        self.height = 112
        self.color = QColor(255, 255, 255)
        self.setFixedSize(self.parent().width(), self.height)

    def setData(self, name: str = 'Фамилия\nИмя\nОтчество', group: str = 'Группа', semester: int = 0,
            curator: str = 'Фамилия И.О.', interval: list = ['01.01.2022', '31.01.2022']):
        self.name = name
        self.group = group
        self.semester = semester
        self.curator = curator
        self.interval = interval

    def paintEvent(self, event):
        leftRightMargin = 16

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Основа
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRect(0, 0, self.parent().width(), self.height)

        # Нижняя граница
        painter.setPen(QPen(QColor(220, 225, 230), 1))
        painter.drawLine(0, self.height, self.parent().width(), self.height)

        # Интервал
        fm = QFontMetrics(QFont('Arial', 8))
        interval = " - ".join(self.interval)
        size = fm.width(interval)

        date_i1 = datetime.strptime(self.interval[0], '%d.%m.%Y')
        date_i2 = datetime.strptime(self.interval[1], '%d.%m.%Y')

        textColor = QColor(132, 138, 150)
        intervalColor = QColor(220, 225, 230)
        painter.setPen(QColor(132, 138, 150))
        intervalImage = QImage(':/icons/icon_calendar.png')

        if datetime.now() > date_i2:
            intervalText = 'Завершена'
        elif datetime.now() < date_i1:
            intervalText = 'Не началась'
        else:
            intervalText = 'Проходит'
            textColor = QColor(255, 255, 255)
            intervalImage = QImage(':/icons/icon_calendar_white.png')

            value = (datetime.now() - date_i1).days * 100 // (date_i2 - date_i1).days
            yellow = 60 * sin(value / 100 * pi)

            r = int(((179 - 75) / 100) * value) + 75 + yellow
            g = int(((179 - 75) / 100) * (100 - value)) + 75 + yellow
            b = 75 - yellow

            intervalColor = QColor(r, g, b)

        painter.setBrush(QBrush(intervalColor))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(leftRightMargin, 81, size + 29, 20, 5.0, 5.0)
        painter.drawImage(QRect(5 + leftRightMargin, 84, 14, 14), intervalImage, QRect(0, 0, 32, 32))

        painter.setFont(QFont('Arial', 8))

        painter.setPen(textColor)
        painter.drawText(QRect(23 + leftRightMargin, 84, fm.width(interval), 22), Qt.TextWordWrap, interval)
        painter.setPen(QColor(132, 138, 150))
        painter.drawText(QRect(self.parent().width() - fm.width(intervalText) - leftRightMargin, 84, self.parent().width() - leftRightMargin, 22), Qt.TextWordWrap, intervalText)

        size = fm.width(f'{self.semester} семестр')

        # группа и семетр
        painter.setFont(QFont('Arial', 8))
        painter.drawText(QRect(self.parent().width() - fm.width(self.group) - leftRightMargin, 10, self.parent().width() - leftRightMargin, 15), Qt.TextWordWrap, self.group)
        painter.drawText(QRect(self.parent().width() - size - leftRightMargin, 38, self.parent().width() - leftRightMargin, 15), Qt.TextWordWrap, f'{self.semester} семестр')

        # Руководитель
        painter.setPen(QColor(132, 138, 150))
        curatorList = self.curator.split(" ")
        curatorText = curatorList[0]

        if len(curatorList) > 1:
            curatorText = curatorText + ' '
            for i in curatorList[1:]:
                curatorText = curatorText + i[0] + '.'

        painter.drawText(QRect(leftRightMargin, 62, self.parent().width() - leftRightMargin, 15), Qt.TextWordWrap, f'Руководитель: {curatorText}')

        # ФИО
        painter.setFont(QFont('Arial', 8, QFont.Bold))
        painter.setPen(QColor(26, 34, 47))
        painter.drawText(QRect(leftRightMargin, 10, self.parent().width() - leftRightMargin, 42), Qt.TextWordWrap, self.name.replace(' ', '\n'))

        painter.end()

    def leaveEvent(self, event):
        self.color = QColor(255, 255, 255)
        self.update()

    def enterEvent(self, event):
        self.color = QColor(245, 246, 248)
        self.update()

