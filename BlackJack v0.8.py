# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import requests
import sys
import copy
from time import sleep

my_hand = []     #карты у меня на руке
comp_hand = []   #карты у компа на руке
now_score = 0     #очки
my_score = 0     #мои очки (для подсчета если игрок не брал карт)

#делаем запрос новой колоды и получаем id колоды:
req = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
shuffle = req.json()
deckID = shuffle['deck_id']



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("BlackJack")
        MainWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lcdMy_score = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdMy_score.setGeometry(QtCore.QRect(20, 30, 101, 41))
        self.lcdMy_score.setObjectName("lcdMy_score")
        self.YButton = QtWidgets.QPushButton(self.centralwidget)
        self.YButton.setGeometry(QtCore.QRect(70, 362, 101, 41))
        self.YButton.setObjectName("YButton")
        self.NButton = QtWidgets.QPushButton(self.centralwidget)
        self.NButton.setGeometry(QtCore.QRect(310, 362, 91, 41))
        self.NButton.setObjectName("NButton")
        self.labNew_card = QtWidgets.QLabel(self.centralwidget)
        self.labNew_card.setGeometry(QtCore.QRect(50, 90, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.labNew_card.setFont(font)
        self.labNew_card.setObjectName("labNew_card")
        self.labNew_score = QtWidgets.QLabel(self.centralwidget)
        self.labNew_score.setGeometry(QtCore.QRect(50, 150, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.labNew_score.setFont(font)
        self.labNew_score.setObjectName("labNew_score")
        self.labMy_hand = QtWidgets.QLabel(self.centralwidget)
        self.labMy_hand.setGeometry(QtCore.QRect(50, 210, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.labMy_hand.setFont(font)
        self.labMy_hand.setObjectName("labMy_hand")
        self.labNow_score = QtWidgets.QLabel(self.centralwidget)
        self.labNow_score.setGeometry(QtCore.QRect(50, 270, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.labNow_score.setFont(font)
        self.labNow_score.setObjectName("labNow_score")
        self.lcdComp_score = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdComp_score.setGeometry(QtCore.QRect(370, 30, 101, 41))
        self.lcdComp_score.setObjectName("lcdComp_score")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.click()


    def click(self):        #нажатие кнопок
        self.YButton.clicked.connect(self.my_take)
        self.NButton.clicked.connect(self.comp_take)

    def my_take(self):
        global now_score
        new_card = take()
        my_hand.append(new_card)
        new_score = card_to_score(new_card)
        global my_score
        now_score = now_score + new_score
        my_score = copy.deepcopy(now_score)
        # вывод данных
        self.labNew_card.setText('Вы вытянули: ' + str(new_card))
        self.labNew_score.setText("Это " + str(new_score) + ' очков')
        self.labMy_hand.setText('У вас на руках: '+str(my_hand))
        self.labNow_score.setText('Всего очков у вас '+str(my_score))
        self.lcdMy_score.display(my_score)
        self.blackjack(now_score)

    def comp_take(self):
        global now_score
        now_score = 0
        while now_score < 14:
            new_card = take()
            comp_hand.append(new_card)
            new_score = card_to_score(new_card)
            now_score = now_score + new_score
            global comp_score
            comp_score = copy.deepcopy(now_score)
            self.labNew_card.setText('Я вытянул: ' + str(new_card))
            self.labNew_score.setText("Это " + str(new_score) + ' очков')
            self.labMy_hand.setText('У меня на руках: ' + str(comp_hand))
            self.labNow_score.setText('Всего очков у меня ' + str(comp_score))
            self.lcdComp_score.display(comp_score)
            self.blackjack(now_score)
        win_or_lose()


    def blackjack(self, now_score):  # проверяем на перебор или очко
        if now_score == 21:
            msg_BJ()
        elif now_score > 21:
            msg_Perebor()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.YButton.setText(_translate("MainWindow", "Ещё карту"))
        self.NButton.setText(_translate("MainWindow", "Хватит"))
        self.labNew_card.setText(_translate("MainWindow", "Новая карта"))
        self.labNew_score.setText(_translate("MainWindow", "Очков получено"))
        self.labMy_hand.setText(_translate("MainWindow", "У вас на руках"))
        self.labNow_score.setText(_translate("MainWindow", "Очков всего"))

def take():             #функция получения и парсинга новой карты из колоды
    req = requests.get('https://deckofcardsapi.com/api/deck/'+deckID+'/draw/?count=1')
    cardJS = req.json()
    cardList = cardJS['cards']
    cardDict = cardList[0]
    card = cardDict['value']
    return card

def card_to_score(new_card):    #функция подсчета очков новой карты
    if new_card == "JACK" or new_card == "QUEEN" or new_card == "KING":
        score = 10
    elif new_card == "ACE":
            if now_score+11> 21:
               score = 1
            else:
               score = 11
    else:
        score = int(new_card)
    return score

def win_or_lose():      #функция выбора победителя и вызова окна с соответствующим сообщением
    sleep(3)
    if my_score < comp_score:
        end = 'Я победил!!! УРА!!! Слава роботам!!!'
    if my_score > comp_score:
        end = 'Ты победил!!! Тебе просто повезло!!!'
    if my_score == comp_score:
        end = 'Ничья! Ну ничего, в следующий раз я у тебя выиграю!!!'
    msg_End(end)

def msg_End(end):              #окно с сообщением в конце игры
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText('У тебя '+str(my_score)+' очков!\nА у меня '+str(comp_score)+' очков!\n'+end)
    msg.setWindowTitle("Итог игры")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    retval = msg.exec_()
    sys.exit()


def msg_BJ():       #окно-сообщение очко!
    sleep(2)
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Собрано 21 очко! Конец игры!")
    msg.setWindowTitle("Очко!")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    retval = msg.exec_()
    sys.exit()

def msg_Perebor():      #окно-сообщение о преборе
    sleep(2)
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setStyleSheet("background-color: red")
    # setting message for Message Box
    msg.setText("<b>Перебор!!!</b>")
    # setting Message box window title
    msg.setWindowTitle("Перебор")
    # declaring buttons on Message Box
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    # start the app
    retval = msg.exec_()
    sys.exit()




#if __name__ == "__main__":
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec())


