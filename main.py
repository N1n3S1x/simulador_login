import json
import datetime
import os
from cryptography.fernet import Fernet

# Diretório base dos arquivos
PASTA_BASE = 'simulador_login'

# Caminhos completos dos arquivos dentro da pasta
USUARIOS_FILE = os.path.join(PASTA_BASE, 'usuario.json')
LOG_FILE = os.path.join(PASTA_BASE, 'log_acesso.txt')
CHAVE_FILE = os.path.join(PASTA_BASE, 'chave.key')

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

def carregar_usuarios(fernet):
    if not os.path.exists(USUARIOS_FILE):
        return {}
    with open(USUARIOS_FILE, 'r') as f:
        dados_criptografados = json.load(f)
    usuarios = {}
    for usuario, senha_enc in dados_criptografados.items():
        senha = fernet.decrypt(senha_enc.encode()).decode()
        usuarios[usuario] = senha
    return usuarios

def salvar_usuarios(usuarios, fernet):
    dados_criptografados = {
        usuario: fernet.encrypt(senha.encode()).decode()
        for usuario, senha in usuarios.items()
    }
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(dados_criptografados, f, indent=4)

def registrar_log(usuario, sucesso, acao='LOGIN'):
    with open(LOG_FILE, 'a') as f:
        agora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'SUCESSO' if sucesso else 'FALHA'
        f.write(f"[{agora}] AÇÃO: {acao} - Usuário: {usuario} - {status}\n")

def fazer_login(usuarios):
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    if usuario in usuarios and usuarios[usuario] == senha:
        print("Login bem-sucedido!")
        registrar_log(usuario, True, acao='LOGIN')
    else:
        print("Usuário ou senha inválidos.")
        registrar_log(usuario, False, acao='LOGIN')

def cadastrar_usuario(usuarios, fernet):
    usuario = input("Novo usuário: ")
    if usuario in usuarios:
        print("Usuário já existe.")
        registrar_log(usuario, False, acao='CADASTRO')
        return
    senha = input("Senha: ")
    confirmacao = input("Confirme a senha: ")
    if senha != confirmacao:
        print("Senhas não conferem.")
        registrar_log(usuario, False, acao='CADASTRO')
        return
    usuarios[usuario] = senha
    salvar_usuarios(usuarios, fernet)
    print(f"Usuário '{usuario}' cadastrado com sucesso.")
    registrar_log(usuario, True, acao='CADASTRO')

def main():
    garantir_pasta()
    gerar_chave()
    chave = carregar_chave()
    fernet = Fernet(chave)

    usuarios = carregar_usuarios(fernet)
    print("Bem-vindo ao simulador de login com criptografia!\n")
    
    while True:
        print("\n[1] Login")
        print("[2] Cadastrar novo usuário")
        print("[0] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            fazer_login(usuarios)
        elif opcao == '2':
            cadastrar_usuario(usuarios, fernet)
            usuarios = carregar_usuarios(fernet)
        elif opcao == '0':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
