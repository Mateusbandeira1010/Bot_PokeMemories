import json
import pyautogui
import time
import random

def cavebot():
    with open("direcoes.json") as f:
        direcoes = json.load(f)

    print(f"{len(direcoes)} direções carregadas. Iniciando Cavebot...\n")

    for passo in direcoes:
        tecla = passo["tecla"]
        x, y = passo["posicao"]
        
        print(f"Movendo para ({x}, {y}) com a tecla '{tecla.upper()}'")
        pyautogui.moveTo(x, y)
        pyautogui.press(tecla)

if __name__ == "__main__":
    cavebot()
