import pyautogui
import time
from pynput.keyboard import Controller, Key, Listener as KeyboardListener
import win32api, win32con
import threading
import random
import tkinter as tk
from tkinter import messagebox

# Configurações globais
TECLA_PESCA = Key.f11
TECLA_EMERGENCIA = Key.f12
keyboard_controller = Controller()
POS_AGUA = []
pescando = False
bot_rodando = False
ataque_ativo = False
clicando_agua = True
interromper_cliques = False
TEMPO_ESPERA = 60
POS_PIXEL = (896, 353)

# Funções de controle do mouse
def click_na_agua_com_ctrl(pos):
    global clicando_agua, interromper_cliques
    if not clicando_agua or interromper_cliques:
        interromper_cliques = False
        return
        
    x, y = pos
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

def click_com_direito(pos):
    global clicando_agua, interromper_cliques
    if not clicando_agua or interromper_cliques:
        interromper_cliques = False
        return
        
    x, y = pos
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

def verificar_pixel():
    time.sleep(1)
    cor_pixel = pyautogui.screenshot().getpixel(POS_PIXEL)
    print(f"A cor do pixel na posição {POS_PIXEL} é: {cor_pixel}")
    cor_esperada = (245, 45, 30)
    if cor_pixel == cor_esperada:
        print("✅ Pixel com cor esperada! Continuando a pesca...")
        return True
    else:
        print("❌ Pixel com cor diferente. Pode estar fora da água ou falhou a pesca.")
        return False

def on_press(key):
    global clicando_agua, interromper_cliques
    if key == TECLA_EMERGENCIA:
        clicando_agua = not clicando_agua
        if not clicando_agua:
            interromper_cliques = True
        estado = "DESATIVADOS" if not clicando_agua else "ATIVADOS"
        print(f"⚠️ Cliques na água {estado} (Tecla F12 pressionada)")
    return True

def jogar_varinha_se_nao_pescando():
    global pescando, bot_rodando
    while True:
        if bot_rodando:
            if not pescando:
                print("⛔ Jogador não está pescando, tentando novamente com hotkey...")
                keyboard_controller.press(TECLA_PESCA)
                keyboard_controller.release(TECLA_PESCA)
                time.sleep(30)
            else:
                time.sleep(5)
        else:
            time.sleep(1)

def bot_de_pesca():
    global pescando, bot_rodando, POS_AGUA, interromper_cliques
    i = 0
    while True:
        if bot_rodando and POS_AGUA:
            pescando = True
            pos_atual = POS_AGUA[i % len(POS_AGUA)]['pos']
            left_clicks = POS_AGUA[i % len(POS_AGUA)]['left_clicks']
            right_clicks = POS_AGUA[i % len(POS_AGUA)]['right_clicks']
            
            print(f"🎣 Pescando na posição {pos_atual} ({left_clicks}x esquerdo, {right_clicks}x direito)...")

            for _ in range(left_clicks):
                if interromper_cliques:
                    interromper_cliques = False
                    break
                    
                keyboard_controller.press(TECLA_PESCA)
                keyboard_controller.release(TECLA_PESCA)
                time.sleep(0.2)
                click_na_agua_com_ctrl(pos_atual)
                time.sleep(0.5)

            for _ in range(right_clicks):
                if interromper_cliques:
                    interromper_cliques = False
                    break
                    
                keyboard_controller.press(TECLA_PESCA)
                keyboard_controller.release(TECLA_PESCA)
                time.sleep(0.2)
                click_com_direito(pos_atual)
                time.sleep(0.5)

            if verificar_pixel():
                print(f"⏳ Aguardando {TEMPO_ESPERA} segundos antes de mudar de posição...\n")
                time.sleep(TEMPO_ESPERA)
            else:
                print("❌ Pixel não detectado corretamente, pulando posição...")

            i += 1
        else:
            pescando = False
            time.sleep(1)

def ataque_automatico():
    global ataque_ativo
    teclas_ataque = [
        Key.f1, Key.f2, Key.f3, Key.f4, Key.f5,
        Key.f6, Key.f7, Key.f8, Key.f9, Key.f10
    ]
    while True:
        if ataque_ativo:
            while ataque_ativo:
                for tecla in teclas_ataque:
                    keyboard_controller.press(tecla)
                    keyboard_controller.release(tecla)
                    time.sleep(0.3)
        else:
            time.sleep(1)

class FishingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎣 Bot de Pesca Avançado")
        self.root.geometry("500x550")
        
        self.left_clicks = tk.IntVar(value=2)
        self.right_clicks = tk.IntVar(value=40)
        self.positions_list = []
        
        # Interface gráfica (conforme seu código original)
        frame_add = tk.LabelFrame(root, text="Adicionar Posição", padx=5, pady=5)
        frame_add.pack(pady=10, padx=10, fill="x")
        
        tk.Label(frame_add, text="Cliques Esquerdo:").grid(row=0, column=0, padx=5)
        tk.Spinbox(frame_add, from_=0, to=10, textvariable=self.left_clicks, width=5).grid(row=0, column=1, padx=5)
        
        tk.Label(frame_add, text="Cliques Direito:").grid(row=0, column=2, padx=5)
        tk.Spinbox(frame_add, from_=0, to=100, textvariable=self.right_clicks, width=5).grid(row=0, column=3, padx=5)
        
        tk.Button(frame_add, text="Pegar Posição Atual", command=self.save_position, bg="blue", fg="white").grid(row=0, column=4, padx=10)
        
        frame_list = tk.LabelFrame(root, text="Posições Salvas", padx=5, pady=5)
        frame_list.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.listbox = tk.Listbox(frame_list, width=50, height=10)
        self.listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(frame_list, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)
        
        tk.Button(frame_buttons, text="Remover Selecionado", command=self.remove_position, bg="orange").grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="Limpar Tudo", command=self.clear_positions, bg="red", fg="white").grid(row=0, column=1, padx=5)
        
        frame_control = tk.LabelFrame(root, text="Controle do Bot", padx=5, pady=5)
        frame_control.pack(pady=10, padx=10, fill="x")
        
        self.status_label = tk.Label(frame_control, text="🔌 Bot de pesca DESLIGADO.", fg="blue")
        self.status_label.pack()
        
        tk.Button(frame_control, text="Ligar Bot de Pesca", command=self.start_bot, bg="green", fg="white", width=20).pack(side="left", padx=5)
        tk.Button(frame_control, text="Desligar Bot de Pesca", command=self.stop_bot, bg="red", fg="white", width=20).pack(side="left", padx=5)
        
        frame_attack = tk.LabelFrame(root, text="Ataque Automático", padx=5, pady=5)
        frame_attack.pack(pady=10, padx=10, fill="x")
        
        self.attack_label = tk.Label(frame_attack, text="🛑 Ataque automático DESLIGADO.", fg="darkred")
        self.attack_label.pack()
        
        tk.Button(frame_attack, text="Ligar Ataque", command=self.start_attack, bg="orange", fg="white", width=20).pack(side="left", padx=5)
        tk.Button(frame_attack, text="Desligar Ataque", command=self.stop_attack, bg="gray", fg="white", width=20).pack(side="left", padx=5)
        
        frame_emergency = tk.LabelFrame(root, text="Controle de Emergência", padx=5, pady=5)
        frame_emergency.pack(pady=10, padx=10, fill="x")
        
        tk.Label(frame_emergency, text="Pressione F12 para pausar/retomar os cliques na água", fg="red").pack()
        self.emergency_status = tk.Label(frame_emergency, text="Status: Cliques ATIVADOS", fg="green")
        self.emergency_status.pack()
    
    def save_position(self):
        x, y = win32api.GetCursorPos()
        left = self.left_clicks.get()
        right = self.right_clicks.get()
        
        position = {
            'pos': (x, y),
            'left_clicks': left,
            'right_clicks': right
        }
        
        self.positions_list.append(position)
        self.update_listbox()
        messagebox.showinfo("Posição Salva", f"Posição {x},{y} salva com {left} cliques esquerdo e {right} cliques direito!")
    
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, pos in enumerate(self.positions_list, 1):
            x, y = pos['pos']
            left = pos['left_clicks']
            right = pos['right_clicks']
            self.listbox.insert(tk.END, f"{idx}. Pos: ({x}, {y}) - Esq: {left}x, Dir: {right}x")
    
    def remove_position(self):
        try:
            selected = self.listbox.curselection()[0]
            self.positions_list.pop(selected)
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Aviso", "Nenhuma posição selecionada!")
    
    def clear_positions(self):
        global POS_AGUA
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todas as posições?"):
            self.positions_list = []
            POS_AGUA = []
            self.update_listbox()
    
    def start_bot(self):
        global bot_rodando, POS_AGUA
        if not self.positions_list:
            messagebox.showerror("Erro", "Adicione pelo menos uma posição antes de iniciar o bot!")
            return
        
        POS_AGUA = self.positions_list.copy()
        bot_rodando = True
        self.status_label.config(text="✅ Bot de pesca ATIVO!", fg="green")
    
    def stop_bot(self):
        global bot_rodando
        bot_rodando = False
        self.status_label.config(text="⛔ Bot de pesca DESLIGADO.", fg="red")
    
    def start_attack(self):
        global ataque_ativo
        ataque_ativo = True
        self.attack_label.config(text="⚔️ Ataque automático ATIVO!", fg="green")
    
    def stop_attack(self):
        global ataque_ativo
        ataque_ativo = False
        self.attack_label.config(text="🛑 Ataque automático DESLIGADO.", fg="darkred")
    
    def update_emergency_status(self, status):
        if status:
            self.emergency_status.config(text="Status: Cliques ATIVADOS", fg="green")
        else:
            self.emergency_status.config(text="Status: Cliques PAUSADOS", fg="red")

def start_threads():
    threading.Thread(target=bot_de_pesca, daemon=True).start()
    threading.Thread(target=jogar_varinha_se_nao_pescando, daemon=True).start()
    threading.Thread(target=ataque_automatico, daemon=True).start()
    threading.Thread(target=start_keyboard_listener, daemon=True).start()

def start_keyboard_listener():
    with KeyboardListener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = FishingBotApp(root)
    
    def update_ui_status():
        app.update_emergency_status(clicando_agua)
        root.after(500, update_ui_status)
    
    root.after(500, update_ui_status)
    start_threads()
    root.mainloop()