import json
import os
import boto3
from dotenv import load_dotenv
import time
import functions

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

ec2_client = session.client('ec2')
ec2_iam = session.client('iam')
ec2_resource = session.resource('ec2')

exit = False

try: 
    with open("variables.tfvars.json", "r") as file:
        dicionario = json.load(file)
except:
    dicionario = {
        "users" : [],
        "security_groups" : [],
        "instances" : [],
        "vpc_cidr" : [] 
        }
    
while exit == False:
    
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print(style.WHITE + "Estamos trabalhando na Região " + style.CYAN + "us-east-1 (Norte da Virginia)" + style.WHITE + ". Opções:\n")
    print(style.CYAN + "(0)" + style.WHITE + " Configurar Subnet")
    print(style.CYAN + "(1)" + style.WHITE + " Criar Usuário")
    print(style.CYAN + "(2)" + style.WHITE + " Criar Instância")
    print(style.CYAN + "(3)" + style.WHITE + " Criar Security Group")
    print(style.CYAN + "(4)" + style.WHITE + " Deletar Instância")
    print(style.CYAN + "(5)" + style.WHITE + " Deletar Security Group")
    print(style.CYAN + "(6)" + style.WHITE + " Listar Instraestrutura")
    print(style.CYAN + "(7)" + style.WHITE + " Sair\n")
    
    escolha = int(input(style.CYAN + "Digite a opção escolhida: " + style.WHITE))
    time.sleep(1)
    
    todas_instancias = dicionario["instances"]
    grupos_de_seguranca = dicionario["security_groups"]
    
    # -------------------------------------------------------------------- Configurando Sub-Rede
    if escolha == 0:
        vpc_cidr = input("\nInsira o VPC cidr: ")
        dicionario["vpc_cidr"] = vpc_cidr
        
        print(style.MAGENTA + "\nEscrevendo Instancia no JSON..")
        time.sleep(1)
        
        with open("variables.tfvars.json", "w") as file:
            json.dump(dicionario, file)
        time.sleep(2)
        
    # -------------------------------------------------------------------- Criando um Usuario 
    elif escolha == 1:
        print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
        
        username = input("Digite o" + style.CYAN + " username " + style.WHITE + "desejado: ")
        decision_username = input("\nDeseja criar restrições? [Y/N]: ")
        while decision_username != "Y" or decision_username != "N":
            decision_username = input("\nDeseja criar restrições? [Y/N]: ")
            if decision_username == "Y":
                acoes = []
                recursos = []
                restrictions = input("Digite o nome da restrição: ")
                action = input("\nDigite as ações da restrição(e.g. ec2:DescribeInstances, ec2:DescribeRegions): \n")
                resources = input("\nColoque os recursos que deseja: ")
                list_actions = acoes.split(",")
                list_resources = recursos.split(",")
                dicionario["users"].append({"username": username, "restrictions": {"restriction_name": restrictions, "actions": list_actions, "resources": list_resources}})
            elif decision_username == "N":
                dicionario["users"].append({"username" : username})
            
        print(style.MAGENTA + "\nEscrevendo usuário no JSON..")
        time.sleep(1)
        
        with open("variables.tfvars.json", "w") as file:
            json.dump(dicionario, file)
            
    # -------------------------------------------------------------------- Criando uma Instancia Nova 
    elif escolha == 2 :
        
        print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
        print("Vamos criar uma nova instância\n")
        
        instance_name = input("Nome da Instância: ")
        
        instance_security_group = input("\nInsira o nome do Security Group: ")
        if instance_security_group in grupos_de_seguranca:
            print("Associando security group {0} à Instancia {1}\n"
                .format(instance_security_group, instance_name))
        else:
            print("Associando security group {0} à Instancia {1}\n"
                .format(instance_security_group, instance_name))
            grupos_de_seguranca.append(instance_security_group)
            
        instance_ami = input("AMI (ex. ami-08c40ec9ead489470): ")
        
        tipo = int(input("\nTipos de Instâncias\n" + style.CYAN + "(1)" + style.WHITE + " t2.micro"
                         + style.CYAN + "\n(2)" + style.WHITE + " t2.nano\n\nTipo: "))
        boolean_tipo = False
        while boolean_tipo == False:
            if tipo == 1:
                instance_type = "t2.micro"
                boolean_tipo = True
            elif tipo == 2:
                instance_type = "t2.nano"
                boolean_tipo = True
            else:
                tipo = int(input("\nTipo não encontrado.\n(1) t2.micro]\n(2) t2.nano]\n\nInsira novamente: "))
                
        instance_region = "us-east-1"
        instance = {
            "name"            : instance_name,
            "security_groups" : instance_security_group,
            "ami"             : instance_ami,
            "instance_type"   : instance_type,
            "region"          : instance_region
            }
        
        todas_instancias.append(instance)
        
        decision_instance = input("\nDeseja confirmar as mudanças? [Y/N] ")
        while decision_instance != "Y" and decision_instance != "N":
            decision_instance = input("\nDeseja confirmar as mudanças? [Y/N]")   
        if decision_instance == "Y":
            
            time.sleep(0.4)
            print(style.MAGENTA + "\nEscrevendo Instancia no JSON..\n" + style.WHITE)

            with open("variables.tfvars.json", "w") as file:
                json.dump(dicionario, file)
            time.sleep(1)
               
            print("Subindo Mudanças no " + style.MAGENTA + "Terraform")
            #os.system('terraform plan -var-file="variables.tfvars.json"')
            time.sleep(2)
            #os.system('terraform apply -var-file="variables.tfvars.json"')
            time.sleep(2)
        elif decision_instance == "N":
            print("\nInstância nāo criada!")
            time.sleep(2)
            pass
    
    # -------------------------------------------------------------------- Criando Security Group
    elif escolha == 3 :
        print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
        
        security_group_id = input("ID do grupo de segurança: ")  
        security_group_name = input("\nNome do grupo de segurança: ")  
        security_group_description = input("\nDescrição do grupo de segurança: ")  

    # -------------------------------------------------------------------- Deletando Instância
    elif escolha == 4 :
        print("")
        print(style.CYAN + "*"*100 + style.WHITE)
        print("4")
    # -------------------------------------------------------------------- Deletando Security Group
    elif escolha == 5 :
        print("")
        print(style.CYAN + "*"*100 + style.WHITE)
        print("5")
    # -------------------------------------------------------------------- Listando Infra   
    elif escolha == 6:
        print("")
        print(style.CYAN + "*"*100 + style.WHITE)
        print("6")
    # -------------------------------------------------------------------- EXIT
    elif escolha == 7:
        exit = True