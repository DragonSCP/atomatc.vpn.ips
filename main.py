import paramiko
import os
import requests

# URLs dos arquivos de IPs das operadoras
URLS_OPERADORAS = {
    'claro': 'https://github.com/DragonSCP/atomatc.vpn.ips/raw/main/operadoras/claro.txt',
    'vivo': 'https://github.com/DragonSCP/atomatc.vpn.ips/raw/main/operadoras/vivo.txt',
    'tim': 'https://github.com/DragonSCP/atomatc.vpn.ips/raw/main/operadoras/tim.txt'
}

def carregar_ips_online(operadora):
    url = URLS_OPERADORAS.get(operadora)
    if not url:
        print(f"URL para a operadora '{operadora}' não encontrada.")
        return []

    try:
        response = requests.get(url)
        response.raise_for_status()
        ips = [linha.strip() for linha in response.text.splitlines()]
        return ips
    except requests.RequestException as e:
        print(f"Erro ao carregar IPs da URL {url}: {e}")
        return []

def carregar_ips_local(operadora):
    caminho_arquivo = os.path.join('operadoras', f'{operadora}.txt')
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo para a operadora '{operadora}' não encontrado.")
        return []

    with open(caminho_arquivo, 'r') as file:
        ips = [linha.strip() for linha in file.readlines()]
    return ips

def testar_ssh(proxy_ip, user, senha):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(proxy_ip, username=user, password=senha)
        print(f"Conectado com sucesso ao proxy {proxy_ip}")
        return True
    except Exception as e:
        print(f"Falha ao conectar ao proxy {proxy_ip}: {e}")
        return False
    finally:
        client.close()

def menu():
    print("Selecione uma opção:")
    print("1. Adicionar e testar um IP de proxy")
    print("2. Testar todos os IPs de uma operadora")

    opcao = int(input("Digite o número da opção: "))

    if opcao == 1:
        operadoras = ['claro', 'vivo', 'tim']
        print("Selecione uma operadora:")
        for idx, operadora in enumerate(operadoras, 1):
            print(f"{idx}. {operadora.capitalize()}")

        escolha = int(input("Digite o número da operadora: "))
        operadora_selecionada = operadoras[escolha - 1].lower()

        proxy_ip = input("Digite o proxy IP que deseja testar: ")
        user = input("Digite o nome de usuário para o SSH: ")
        senha = input("Digite a senha para o SSH: ")

        testar_ssh(proxy_ip, user, senha)
    
    elif opcao == 2:
        operadoras = ['claro', 'vivo', 'tim']
        print("Selecione uma operadora:")
        for idx, operadora in enumerate(operadoras, 1):
            print(f"{idx}. {operadora.capitalize()}")

        escolha = int(input("Digite o número da operadora: "))
        operadora_selecionada = operadoras[escolha - 1].lower()

        ips_real = carregar_ips_online(operadora_selecionada)
        if not ips_real:
            print("Nenhum IP disponível para teste.")
            return

        proxy_ip = input("Digite o proxy IP que deseja usar para os testes: ")
        user = input("Digite o nome de usuário para o SSH: ")
        senha = input("Digite a senha para o SSH: ")

        for ip in ips_real:
            print(f"Testando IP: {ip}")
            testar_ssh(ip, user, senha)
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    menu()
