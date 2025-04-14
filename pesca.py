from pynput.keyboard import Controller, Key
import win32api, win32con
import threading
import time
import random
import pyautogui


TECLA_PESCA = Key.f11
keyboard_controller = Controller()


POS_AGUA = [
    (817, 246),
    (728, 176),
    (771, 194)
]

pescando = True

TEMPO_ESPERA = 5

def click_na_agua_com_ctrl(pos):
    x, y = pos

    
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
   
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
 
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

def bot_de_pesca():
    global pescando
    i = 0
    while True:
        if pescando:
            pos_atual = POS_AGUA[i % len(POS_AGUA)]
            print(f"🎣 Usando vara de pesca com hotkey na posição {pos_atual}...")

            keyboard_controller.press(TECLA_PESCA)
            keyboard_controller.release(TECLA_PESCA)

            time.sleep(0.2)
            click_na_agua_com_ctrl(pos_atual)

            print(f"Aguardando {TEMPO_ESPERA} segundos antes de tentar novamente...\n")
            time.sleep(TEMPO_ESPERA)

            i += 1
        else:
            time.sleep(0.5)

def main():
    print("Bot de pesca iniciado. Pressione CTRL+C para parar")
    threading.Thread(target=bot_de_pesca, daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
