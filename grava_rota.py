import json
import pyautogui
from pynput import keyboard

rota = []

def on_press(key):
    try:
        tecla = key.char.lower()
        if tecla in ['w', 'a', 's', 'd']:
            x, y = pyautogui.position()
            rota.append({'tecla': tecla, 'posicao': (x, y)})
            print(f"Registrado: tecla '{tecla.upper()}' no SQM ({x}, {y})")
    except AttributeError:
    
        if key == keyboard.Key.f8:
            with open("rota.json", "w") as f:
                json.dump(rota, f, indent=4)
            print("Gravação finalizada. Arquivo 'rota.json' salvo!")
            return False  

with keyboard.Listener(on_press=on_press) as listener:
    print("Gravando rota. Use W, A, S, D para registrar. Pressione F8 para salvar e sair.")
    listener.join()
