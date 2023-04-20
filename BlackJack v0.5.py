import requests
import copy
import sys
from time import sleep

my_hand = []        #карты на руке
now_score = 0     #очки на руке в период добора

#делаем запрос новой колоды и получаем id колоды:
req = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
shuffle = req.json()
deckID = shuffle['deck_id']

def take():                     #функция получения новой карты из колоды
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

def blackjack(now_score):   #проверяем на перебор или очко
    if  now_score == 21:
        print("ОЧКО!")
        sys.exit()
    elif now_score > 21:
        print("ПЕРЕБОР!!!")
        sys.exit()
        
#игрок тянет карту:        
a = 'y'
while a == 'y':
    a = input('Ещё карту?  (Y/N):  ')
    if a == 'y':
        new_card = take()
        my_hand.append(new_card)
        new_score = card_to_score(new_card)
        now_score = now_score + new_score
        print('Ты вытянул ', new_card)
        print('это ', new_score, ' очков')
        print('У тебя на руках: ', my_hand)
        print('Это ', now_score, ' очков')
        print()
    blackjack(now_score)
my_score = copy.deepcopy(now_score)

print('Теперь я тяну!')
sleep(1)

#компьютер тянет карту
now_score = 0
while now_score < 14:
    new_card = take()
    my_hand.append(new_card)
    new_score = card_to_score(new_card)
    now_score = now_score + new_score
    print('Я вытянул ', new_card)
    print('это ', new_score, ' очков')
    print('У меня на руках: ', my_hand)
    print('Это ', now_score, ' очков')
    print()
    blackjack(now_score)
    sleep(1)
comp_score = now_score

print('У тебя ',my_score,' очков!')
print('А у меня ',comp_score,' очков!')
if my_score < comp_score:
    print("Я победил!!! УРА!!! Слава роботам!!!")
if my_score > comp_score:
    print('Ты победил!!! Тебе просто повезло!!!')
if my_score == comp_score:
    print('Ничья! Ну ничего, в следующий раз я у тебя выиграю!!!')
