import os
import boto3
import json
from dotenv import load_dotenv

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

print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
print("Para criar uma VPC precisaremos de algumas infos:\n")
print("Regiões disponíveis:")
print(style.CYAN + "(1)" + style.WHITE + " us-east-1")
print(style.CYAN + "(2)" + style.WHITE + " us-east-2\n")

regiao = False
region = int(input(style.CYAN +  "Digite a região escolhida: " + style.WHITE))
while regiao == False:
    if region == 1:
        print(style.MAGENTA + "\nPreparando Ambiente...")
        os.chdir("region1")
        os.system("python3 region1.py")
        regiao = True
    elif region == 2:
        print(style.MAGENTA +  "\nPreparando Ambiente..")
        os.chdir("region2")
        os.system("python3 region2.py")
        regiao = True
    else:
        print("Regiões disponíveis:")
        print(style.CYAN + "(1)" + style.WHITE + " us-east-1")
        print(style.CYAN + "(2)" + style.WHITE + " us-east-2\n")
        print("Insira o número corretamente\n")
        region = input("Digite a região escolhida: ")
        regiao = False