import json
import pyautogui
from pynput import keyboard

rota = []
teclas_validas = ['w', 'a', 's', 'd']
pressionadas = set()

def on_press(key):
    try:
        tecla = key.char.lower()
        if tecla in teclas_validas and tecla not in pressionadas:
            pressionadas.add(tecla)
            x, y = pyautogui.position()
            rota.append({'tecla': tecla, 'posicao': [x, y]})
            print(f"Registrado: tecla '{tecla.upper()}' no SQM ({x}, {y})")
    except AttributeError:
        if key == keyboard.Key.f8:
            with open("direcoes.json", "w") as f:
                json.dump(rota, f, indent=4)
            print("Gravação finalizada. Arquivo 'direcoes.json' salvo!")
            return False

def on_release(key):
    try:
        tecla = key.char.lower()
        if tecla in pressionadas:
            pressionadas.remove(tecla)
    except:
        pass

print("Gravando rota. Use W, A, S, D para registrar. Pressione F8 para salvar e sair.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
