import json
import pyautogui

def cavebot():
    try:
        with open("direcoes.json", "r") as f:
            direcoes = json.load(f)
    except FileNotFoundError:
        print("Arquivo 'direcoes.json' não encontrado.")
        return

    print(f"{len(direcoes)} direções carregadas. Iniciando Cavebot...")

    for i, passo in enumerate(direcoes):
        tecla = passo["tecla"]
        x, y = passo["posicao"]

        print(f"[{i+1}/{len(direcoes)}] Indo para ({x}, {y}) e pressionando '{tecla.upper()}'")
        pyautogui.moveTo(x, y)
        pyautogui.press(tecla)

    print("Caminho finalizado.")

if __name__ == "__main__":
    cavebot()
