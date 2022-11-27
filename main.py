import os
import boto3
import json
from dotenv import load_dotenv
import functions
import time

load_dotenv()   
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

os.system("")

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
global variaveis
global aws_users
global instances
global username
global region
    
variaveis = {"instances" : {},  "security_groups" : {}, "security_group_instances": {}, "aws_region" : ""}
aws_users = {"aws_user_name" : []}
instances = []
username = ""
region = ""

print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
print("Bem Vindo ao Programa! Vamos Começar?\n")
regiao_escolhida = functions.escolhe_regiao()

exit = False
while exit == False:
    
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print(style.WHITE + "Estamos trabalhando na Região " + style.CYAN + 
          "{0}".format(regiao_escolhida) + style.WHITE + ". Opções:\n")

    print(style.CYAN + "(1)" + style.WHITE + " Criar Usuário")
    print(style.CYAN + "(2)" + style.WHITE + " Criar Instância e Security Group")
    print(style.CYAN + "(3)" + style.WHITE + " Iniciar Instancia")
    print(style.CYAN + "(4)" + style.WHITE + " Parar Instancia")
    print(style.CYAN + "(5)" + style.WHITE + " Deletar Instância e Security Group")
    print(style.CYAN + "(6)" + style.WHITE + " Listar Instraestrutura")
    print(style.CYAN + "(7)" + style.WHITE + " Subir mudanças no terraform")
    print(style.CYAN + "(8)" + style.WHITE + " Sair\n")
    
    escolha = input(style.CYAN + "Digite a opção escolhida: " + style.WHITE)
    time.sleep(1)
    
    while escolha != "1" and escolha != "2" and escolha != "3" and escolha != "4" and escolha != "5" and escolha != "6" and escolha != "7" and escolha != "8":
        print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n") 
        print(style.WHITE + "\nEstamos trabalhando na Região " + style.CYAN + 
          "{0}".format(regiao_escolhida) + style.WHITE + ". Opções:\n")

        print(style.CYAN + "(1)" + style.WHITE + " Criar Usuário")
        print(style.CYAN + "(2)" + style.WHITE + " Criar Instância e Security Group")
        print(style.CYAN + "(3)" + style.WHITE + " Iniciar Instancia")
        print(style.CYAN + "(4)" + style.WHITE + " Parar Instancia")
        print(style.CYAN + "(5)" + style.WHITE + " Deletar Instância e Security Group")
        print(style.CYAN + "(6)" + style.WHITE + " Listar Instraestrutura")
        print(style.CYAN + "(7)" + style.WHITE + " Subir mudanças no terraform")
        print(style.CYAN + "(8)" + style.WHITE + " Sair\n")
        
        escolha = input(style.RED + "Número não aceito. " + style.CYAN + "Digite novamente a opção escolhida: " + style.WHITE)
        time.sleep(1)
        
    if escolha == "1":
        functions.cria_usuario()
        time.sleep(2)
    elif escolha == "2":
        functions.cria_instancia(regiao_escolhida)
        time.sleep(2)
    elif escolha == "3":
        functions.inicia_instancia(None, None, regiao_escolhida)
        time.sleep(2)
    elif escolha == "4":
        functions.para_instancia(None, None, regiao_escolhida)
        time.sleep(2)
    elif escolha == "5":
        functions.deletar_recursos()
        time.sleep(2)
    elif escolha == "6":
        functions.listar_recuros(regiao_escolhida)
        time.sleep(2)
    elif escolha == "7":
        functions.sobe_terraform() 
        time.sleep(2)
    elif escolha == "8":
        print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
        print("Terminando Processos...")
        print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
        time.sleep(2)
        exit = True
    
    
    
    
    