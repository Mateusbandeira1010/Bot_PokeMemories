import json
import pyautogui
from pynput import keyboard
import threading
import time

rota = []
pressionadas = set()
teclas_validas = ['w', 'a', 's', 'd']
intervalo = 0.5  # tempo entre capturas (em segundos)
gravando = True

def gravar_tecla(tecla):
    while tecla in pressionadas and gravando:
        x, y = pyautogui.position()
        rota.append({'tecla': tecla, 'posicao': [x, y]})
        print(f"Registrado: tecla '{tecla.upper()}' no SQM ({x}, {y})")
        time.sleep(intervalo)

def on_press(key):
    global gravando
    try:
        tecla = key.char.lower()
        if tecla in teclas_validas and tecla not in pressionadas:
            pressionadas.add(tecla)
            threading.Thread(target=gravar_tecla, args=(tecla,), daemon=True).start()
    except AttributeError:
        if key == keyboard.Key.f8:
            gravando = False
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

print("Modo de caminhada livre ativado.")
print("Segure W, A, S, D para gravar movimento contínuo.")
print("Pressione F8 para salvar e sair.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
