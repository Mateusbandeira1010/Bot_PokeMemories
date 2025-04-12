import pyautogui
import time


X_WATER = 957
Y_WATER = 572
RGB_WATER = (37, 70, 159)

X_FISHING = 600
Y_FISHING = 813
RGB_FISHING = (190, 130, 130)

X_LOOT_POKEMON = 653
Y_LOOT_POKEMON = 426
RGB_LOOT_POKEMON = (35, 99, 24)

X_LOOT_CLICK_LOOT = 1266
Y_LOOT_CLICK_LOOT = 275
RGB_LOOT_CLICK_LOOT = (191, 240, 255)

ATTACK_KEYS = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']

def click_fish():
    pyautogui.click(X_FISHING, Y_FISHING)

def click_water():
    pyautogui.click(X_WATER, Y_WATER)

def attack_pokemon():
    for key in ATTACK_KEYS:
        pyautogui.press(key)
        time.sleep(0.1)

def is_fishing():
    return pyautogui.pixelMatchesColor(X_FISHING, Y_FISHING, RGB_FISHING)

def has_loot():
    return pyautogui.pixelMatchesColor(X_LOOT_POKEMON, Y_LOOT_POKEMON, RGB_LOOT_POKEMON)

def open_and_loot():
    pyautogui.rightClick(X_LOOT_POKEMON, Y_LOOT_POKEMON)
    time.sleep(0.3)  
    if pyautogui.pixelMatchesColor(X_LOOT_CLICK_LOOT, Y_LOOT_CLICK_LOOT, RGB_LOOT_CLICK_LOOT):
        pyautogui.click(X_LOOT_CLICK_LOOT, Y_LOOT_CLICK_LOOT)  

vara_lancada = False

while True:
    if not is_fishing():
        if not vara_lancada:
            click_fish()
            time.sleep(0.3)
            click_water()
            vara_lancada = True
    else:
        vara_lancada = False


    attack_pokemon()

    if has_loot():
        open_and_loot()

    time.sleep(0.5)
