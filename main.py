import sys
import os
import json
import datetime
import sqlite3
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from PySide6.QtCore import Qt
from cryptography.fernet import Fernet
from tela_principal import Ui_Dialog  # Interface gerada do .ui


# === Diretórios e arquivos ===
PASTA_BASE = 'simulador_login'
USUARIOS_FILE = os.path.join(PASTA_BASE, 'usuario.json')
LOG_FILE = os.path.join(PASTA_BASE, 'log_acesso.txt')
CHAVE_FILE = os.path.join(PASTA_BASE, 'chave.key')

# === Utilitários ===

def bancoDados():
    # Conectar ao banco de dados (ou criar um novo se não existir)
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS test
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL)''')
    

def inserirDados(usuario, senha):
    # Conectar ao banco de dados
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    # Inserir dados na tabela
    c.execute("INSERT INTO test (usuario, senha) VALUES (?, ?)", (usuario, senha))

    # Salvar (commit) as mudanças e fechar a conexão
    conn.commit()
    conn.close()

def loginUsuarioBD(usuario, senha):
    # Conectar ao banco de dados
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    # Verificar se o usuário e senha existem na tabela
    query = f"SELECT * FROM test WHERE usuario ='{usuario}' AND senha = '{senha}'"
    print(f"Executando a query: {query}")
    c.execute(query)

    result = c.fetchone()
    if result:
        print("Usuário e senha válidos!")
    else:
        print("Usuário e senha inválidos!")


def garantir_pasta():
    if not os.path.exists(PASTA_BASE):
        os.makedirs(PASTA_BASE)

def gerar_chave():
    if not os.path.exists(CHAVE_FILE):
        chave = Fernet.generate_key()
        with open(CHAVE_FILE, 'wb') as f:
            f.write(chave)

def carregar_chave():
    with open(CHAVE_FILE, 'rb') as f:
        return f.read()

def carregar_usuarios():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT usuario, senha FROM test")
    usuarios = c.fetchall()
    conn.close()
    usuarios = {usuario: senha for usuario, senha in usuarios}
    print(usuarios)
    return usuarios


# def carregar_usuarios(fernet):
#     if not os.path.exists(USUARIOS_FILE):
#         return {}
#     with open(USUARIOS_FILE, 'r') as f:
#         dados_criptografados = json.load(f)
#     usuarios = {}
#     for usuario, senha_enc in dados_criptografados.items():
#         senha = fernet.decrypt(senha_enc.encode()).decode()
#         usuarios[usuario] = senha
#     return usuarios

def salvar_usuarios(usuario, senha):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    
    query = f"INSERT INTO test (usuario, senha) VALUES ('{usuario}', '{senha}')"
    c.execute(query)
    
    c.close()
    conn.commit()
    


# def salvar_usuarios(usuarios, fernet):
#     dados_criptografados = {
#         usuario: fernet.encrypt(senha.encode()).decode()
#         for usuario, senha in usuarios.items()
#     }
#     with open(USUARIOS_FILE, 'w') as f:
#         json.dump(dados_criptografados, f, indent=4)

def registrar_log(usuario, sucesso, acao='LOGIN', mensagem = ''):
    agora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'SUCESSO' if sucesso else 'FALHA'
    log = f"[{agora}] AÇÃO: {acao} - Usuário: {usuario} - {status} - {mensagem}"
    with open(LOG_FILE, 'a') as f:
        f.write(log + '\n')
    return log

# === Classe da Interface ===
class SistemaLogin(QDialog):
    def __init__(self, fernet):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.fernet = fernet
        self.usuarios = carregar_usuarios()
        

        # Conectando botões
        self.ui.pushButton_Login.clicked.connect(self.fazer_login)
        self.ui.pushButton_Registrar.clicked.connect(self.cadastrar_usuario)

    def fazer_login(self):
        usuario = self.ui.lineEdit_Usuario.text()
        senha = self.ui.lineEdit_Senha.text()
        
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
      
        query = f"SELECT * FROM test WHERE usuario ='{usuario}' AND senha = '{senha}'"
        print(f"Executando a query: {query}")
        
        c.execute(query)
        
        result = c.fetchone()
        
        # if result:
        #     log = registrar_log(usuario, True, 'LOGIN', query)
        #     self.ui.textBrowser_Log.append(log)
        #     QMessageBox.information(self, "Login", "Login bem-sucedido!")
        # else:
        #     log = registrar_log(usuario, False, 'LOGIN')
        #     self.ui.textBrowser_Log.append(log)
        #     QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")

        if usuario in self.usuarios and self.usuarios[usuario] == senha:
            log = registrar_log(usuario, True, 'LOGIN')
            self.ui.textBrowser_Log.append(log)
            QMessageBox.information(self, "Login", "Login bem-sucedido!")
        else:
            log = registrar_log(usuario, False, 'LOGIN')
            self.ui.textBrowser_Log.append(log)
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")

    def cadastrar_usuario(self):
        usuario = self.ui.lineEdit_Usuario.text()
        senha = self.ui.lineEdit_Senha.text()
        
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT * FROM test WHERE usuario = ?", (usuario,))
        result = c.fetchone()
        
        if result:
            log = registrar_log(usuario, False, 'CADASTRO')
            self.ui.textBrowser_Log.append(log)
            QMessageBox.warning(self, "Erro", "Usuário já existe.")
            return
        
        # if usuario in self.usuarios:
        #     log = registrar_log(usuario, False, 'CADASTRO')
        #     self.ui.textBrowser_Log.append(log)
        #     QMessageBox.warning(self, "Erro", "Usuário já existe.")
        #     return


        
        salvar_usuarios(usuario, senha)
        
        log = registrar_log(usuario, True, 'CADASTRO')
        self.ui.textBrowser_Log.append(log)
        QMessageBox.information(self, "Cadastro", f"Usuário '{usuario}' cadastrado com sucesso!")
        
        # self.usuarios[usuario] = senha
        # salvar_usuarios(self.usuarios, senha)
        
        # log = registrar_log(usuario, True, 'CADASTRO')
        # self.ui.textBrowser_Log.append(log)
        # QMessageBox.information(self, "Cadastro", f"Usuário '{usuario}' cadastrado com sucesso!")

# === Execução principal ===
def main():
    bancoDados()
    inserirDados('admin', '123456789')
    garantir_pasta()
    gerar_chave()
    chave = carregar_chave()
    fernet = Fernet(chave)

    app = QApplication(sys.argv)
    janela = SistemaLogin(fernet)
    janela.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
