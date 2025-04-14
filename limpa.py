import os

# Função para excluir arquivos
def limpar_arquivos():
    arquivos = ['direcoes.json', 'rota.json']
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"Arquivo '{arquivo}' excluído com sucesso.")
        else:
            print(f"Arquivo '{arquivo}' não encontrado.")

if __name__ == '__main__':
    limpar_arquivos()
