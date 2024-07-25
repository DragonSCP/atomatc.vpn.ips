#!/bin/bash

# Atualize o Termux
pkg update -y
pkg upgrade -y

# Instale pacotes necessários
pkg install -y git python

# Clone o repositório
git clone https://github.com/DragonSCP/atomatc.vpn.ips.git

# Navegue para o diretório do repositório
cd atomatc.vpn.ips

# Instale pip para o Python
pkg install -y python-pip

# Instale as dependências Python
pip install -r requirements.txt

# Caso não exista requirements.txt, instale dependências manualmente
pip install paramiko requests

# Executar o script principal (opcional, se desejar automatizar a execução)
# python main.py
