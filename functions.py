import os
import boto3
import json
from dotenv import load_dotenv
import time

os.system("")

load_dotenv()   
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

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

# ------------------------------------------------------------------------ Cores Usadas no Terminal
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
    
# --------------------------------- TERRAFORM -------------------------------------------

# ------------------------------------------------------------------------ ESCOLHE REGIAO
def escolhe_regiao():
    
    global variaveis
    global aws_users
    global instances
    global username
    global region
    
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print("Para criar uma VPC precisaremos de algumas infos:\n")
    print("Regiões disponíveis:")
    print(style.CYAN + "(1)" + style.WHITE + " us-east-1")
    print(style.CYAN + "(2)" + style.WHITE + " us-west-1\n")

    decisao_regiao = input(style.CYAN +  "Digite a região escolhida: " + style.WHITE)
    while decisao_regiao != "1" and decisao_regiao != "2":
        print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n") 
        print("Regiões disponíveis:")
        print(style.CYAN + "(1)" + style.WHITE + " us-east-1")
        print(style.CYAN + "(2)" + style.WHITE + " us-west-1\n")
        decisao_regiao = input(style.RED + f"Número não aceito. " + style.CYAN + "Digite a região escolhida novamente: " + style.WHITE) 
        time.sleep(1)   
        
    if decisao_regiao == '1':
        region = "us-east-1"
        vpc_cidr_block = "10.0.0.0/16"
        print(style.MAGENTA + "\nPreparando Ambiente...")
        time.sleep(2)
    elif decisao_regiao == '2':
        region = "us-west-1"
        vpc_cidr_block = "172.16.0.0/16" 
        print(style.MAGENTA +  "\nPreparando Ambiente..")
        time.sleep(2)

    arquivo = f'{region}/.auto-{region}.tfvars.json'

    if os.path.exists(arquivo):
        variaveis = carrega_variaveis()
        aws_users = carrega_users()
        instances = [instance for instance in {key for key in variaveis["instances"]}]
    else:
        variaveis = {"instances" : {},  "secutiry_groups" : {}, "security_group_instances": {}, "aws_region" : "", "vpc_cidr_block":""}
        aws_users = {"aws_user_name" : []}
        instances = []

    variaveis.update({str("aws_region") : str(region)})
    variaveis.update({str("vpc_cidr_block") : str(vpc_cidr_block)})
    escreve_variaveis(variaveis)
    return region

# ------------------------------------------------------------------------ CRIA USER

def cria_usuario():
    global username
    global aws_users
    
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print(f"Vamos criar um novo usuário\n")
    username = input("Digite o" + style.CYAN + " username " + style.WHITE + "desejado: ")
    print("\n** Esse user pode trocar senha, criar e parar instâncias\n")

    decisao_restricoes = input(f"Gostaria de criar restrições para essse user? (y/n): ")
    while y_ou_n(decisao_restricoes):
        decisao_restricoes = input(f"Gostaria de criar restrições para essse user? (y/n): ")
    if decisao_restricoes == "y":
        cria_restricao()
    elif decisao_restricoes == "n":
        print(style.MAGENTA + "\nCriando user novo..\n")
        aws_users["aws_user_name"].append({"username": username, "policy_name": "FullAccess_" + username, "policy_description": "All access conceed to the user", "policy_action": ["*"], "policy_resource": "*", "policy_effect": "Allow"})
        escreve_users(aws_users)
        
# ------------------------------------------------------------------------ CRIA RESTRICAO
        
def cria_restricao():
    global aws_users

    list_describe = {
            "Action": [
            "ec2:Describe*",
            "ec2:Get*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }

    list_describe_create =  {
        "Action": [
            "ec2:Describe*",
            "ec2:Get*",
            "ec2:Create*",
            "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
            "ec2:ModifySecurityGroupRules",
            "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
            "ec2:AuthorizeSecurityGroupIngress", 
            "ec2:RevokeSecurityGroupIngress", 
            "ec2:AuthorizeSecurityGroupEgress", 
            "ec2:RevokeSecurityGroupEgress",
            "ec2:RunInstances"
        ],
        "Effect": "Allow",
        "Resource": "*"
        }

    list_describe_create_delete = {
        "Action": [
            "ec2:Describe*",
            "ec2:Get*",
            "ec2:Create*",
            "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
            "ec2:ModifySecurityGroupRules",
            "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
            "ec2:AuthorizeSecurityGroupIngress", 
            "ec2:RevokeSecurityGroupIngress", 
            "ec2:AuthorizeSecurityGroupEgress", 
            "ec2:RevokeSecurityGroupEgress",
            "ec2:RunInstances",
            "ec2:TerminateInstances",
            "ec2:Delete*"
        ],
        "Effect": "Allow",
        "Resource": "*"
        }
    print("Temos as seguintes opções:")
    print(style.CYAN + "(1)" + style.WHITE + " Descrever e Listar")
    print(style.CYAN + "(2)" + style.WHITE + " Descrever, Listar e Criar")
    print(style.CYAN + "(3)" + style.WHITE + " Descrever, Listar, Criar e Destruir")
    decisao_restricao = input(style.CYAN + "Digite a opção escolhida: " + style.WHITE)

    while isNumber(decisao_restricao):
        decisao_restricao = input(style.CYAN + "Digite a opção escolhida: " + style.WHITE)
    if decisao_restricao == "1":
        aws_users["aws_user_name"].append({"username" : username, "policy_name": "ReadOnlyAccess_" + username, "policy_description": "Descrever e listar recursos", 
            "policy_action": list_describe["Action"], "policy_resource": list_describe["Resource"], "policy_effect": list_describe["Effect"]})
        escreve_users(aws_users)
    elif decisao_restricao == "2":
        aws_users["aws_user_name"].append({"username" : username, "policy_name": "ReadWriteAccess_" + username, "policy_description": "Descrever, listar e criar recursos", 
            "policy_action": list_describe_create["Action"], "policy_resource": list_describe_create["Resource"], "policy_effect": list_describe_create["Effect"] })
        escreve_users(aws_users)
    elif decisao_restricao == "3":
        aws_users["aws_user_name"].append({"username" : username, "policy_name": "ReadWriteDeleteAccess_" + username, "policy_description": "Descrever, listar, criar e destroy recursos", 
            "policy_action": list_describe_create_delete["Action"], "policy_resource": list_describe_create_delete["Resource"], "policy_effect": list_describe_create_delete["Effect"] })
        escreve_users(aws_users)

# ------------------------------------------------------------------------ CRIA INSTANCIA

def cria_instancia(region):
    
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print(f"Vamos criar uma nova instância e Security Group\n")
    instance_name = input("Nome da Instância: ")
    instances.append(instance_name)
    print("\nImagens Disponíveis:") 
    print(style.CYAN + "(1)" + style.WHITE + " Ubuntu Server 20.04 LTS")
    print(style.CYAN + "(2)" + style.WHITE + " Ubuntu Server 22.04 LTS\n")
    decisao_imagem = input("Qual Imagem deseja usar? ")

    if decisao_imagem == "1" and region == "us-east-1":
        instance_image = "ami-0149b2da6ceec4bb0"
    elif decisao_imagem == "2" and region == "us-east-1":
        instance_image = "ami-08c40ec9ead489470"
    elif decisao_imagem == "1" and region == "us-west-1":
        instance_image = "ami-03f6d497fceb40069"
    elif decisao_imagem == "2" and region == "us-west-1":
        instance_image = "ami-02ea247e531eb3ce6"
    
    instance_tipo = input("\nTipos de Instâncias\n" + style.CYAN + "(1)" + style.WHITE + " t2.micro"
                         + style.CYAN + "\n(2)" + style.WHITE + " t2.nano\n\nTipo: ")
    boolean_tipo = False
    while boolean_tipo == False:
        if instance_tipo == '1':
            instance_type = "t2.micro"
            boolean_tipo = True
        elif instance_tipo == '2':
            instance_type = "t2.nano"
            boolean_tipo = True
        else:
            instance_tipo = int(input("\nTipo não encontrado.\n(1) t2.micro]\n(2) t2.nano]\n\nInsira novamente: "))

    variaveis["instances"].update({str(instance_name) : {"image_id" : str(instance_image), "instance_type" : str(instance_type)}})
    escreve_variaveis(variaveis)   

    security_group = input(f"\nGostaria de criar um novo Security Group? (y/n) ")

    while y_ou_n(security_group):
        security_group = input(f"\nGostaria de criar um novo Security Group? (y/n) ") 
    if security_group == "y":
        cria_security_group(instance_name)
    elif security_group == "n":
        print(f"Vamos utilizar o modo default")
        cria_security_group_default(instance_name)
        
# ------------------------------------------------------------------------ CRIA SECURITY GROUP
        
def cria_security_group(instance_name):
    
    lista_group_name = []
    
    print("\nVamos Criar Grupos de Segurança\n")

    security_group_name = input(f"Nome do Security Group: ")

    n_rules = int(input(f"\nQuantas regras deseja? "))

    dict_standard_rule = {"ingress" : {"description" : "Allow inbound traffic", \
                        "from_port" : 0, \
                        "to_port" : 0, \
                        "protocol" : -1, \
                        "ipv6_cidr_blocks" : None, \
                        "prefix_list_ids" : None, \
                        "self" : None , \
                        "security_groups" : None , \
                        "cidr_blocks" : ["0.0.0.0/0"]}}

    regras = [dict_standard_rule]

    for i in range(int(n_rules)):
        description_security_group = input("Description: ")
        aws_from_port = input("\nStart port: ")
        aws_to_port = input("\nEnd port: ")
        aws_protocol = input("\nProtocol: ")
        aws_cidr_blocks = input("\nCIDR Block: ")

        dic_regras = {"ingress" : {"description" : str(description_security_group), \
                                    "from_port" : str(aws_from_port), 
                                    "to_port" : str(aws_to_port), \
                                    "protocol" : str(aws_protocol), 
                                    "ipv6_cidr_blocks" : None,  \
                                    "prefix_list_ids" : None,  \
                                    "self" : None,  \
                                    "security_groups" : None,  \
                                    "cidr_blocks" : [str(aws_cidr_blocks)]}}
        
        regras.append(dic_regras)

        variaveis["security_groups"].update({str(security_group_name) : {"name" : security_group_name, "ingress": regras}})
        escreve_variaveis(variaveis)

        print("Vamos linkar a security group com a Instancia")
        variaveis["security_group_instances"].update({instance_name : {"security_names" : security_group_name}})

    escreve_variaveis(variaveis)

def cria_security_group_default(instance_name):

    regras = []
    dic_regras = {"ingress" : {"description" : "Allow inbound traffic", \
                                "from_port" : 0, \
                                "to_port" : 0, \
                                "protocol" : -1, \
                                "ipv6_cidr_blocks" : None, \
                                "prefix_list_ids" : None, \
                                "self" : None , \
                                "security_groups" : None , \
                                "cidr_blocks" : ["0.0.0.0/0"]}}
            
    regras.append(dic_regras)
    variaveis["security_groups"].update({"standard" : {"name" : "standard", "ingress": regras}})
    escreve_variaveis(variaveis)

    for i in range(len(instances)):
        if instances[i] == instance_name:
            variaveis["security_group_instances"].update({str(instances[i]) : {"security_names" : ["standard"]}})
            escreve_variaveis(variaveis)

# ------------------------------------------------------------------------ INCIA INSTANCIA

def inicia_instancia(event, context, region):
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print(f"Vamos Iniciar um Instância\n")
    instances = input(f"ID da Instância: ")
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    print('Iniciando as Instâncias: ' + str(instances))

# ------------------------------------------------------------------------ PARA INSTANCIA

def para_instancia(event, context, region):
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print(f"Vamos Parar um Instância\n")
    instances = [input("ID da Instância: ")]
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=instances)
    print('Instancia parada: ' + str(instances))

# ------------------------------------------------------------------------ DELETA RECURSOS

def deletar_recursos():

    variaveis = carrega_variaveis()
    aws_users = carrega_users()
    
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print("Deleções Disponíveis:")
    print(style.CYAN + "(1)" + style.WHITE + " Instâncias")
    print(style.CYAN + "(2)" + style.WHITE + " Security Group")
    print(style.CYAN + "(3)" + style.WHITE + " Regra de Security Group")
    print(style.CYAN + "(4)" + style.WHITE + " User")
    decisao_deletar = input(style.CYAN + "\nInsira qual deseja deletar: " + style.WHITE)
    
    while decisao_deletar != "1" and decisao_deletar != "2" and decisao_deletar != "3" and decisao_deletar != "4":
        print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
        print("Deleções Disponíveis:")
        print(style.CYAN + "(1)" + style.WHITE + " Instâncias")
        print(style.CYAN + "(2)" + style.WHITE + " Security Group")
        print(style.CYAN + "(3)" + style.WHITE + " Regra de Security Group")
        print(style.CYAN + "(4)" + style.WHITE + " User")
        decisao_deletar = input(style.RED + "\nNúmero não aceito. " + style.CYAN + "Insira qual deseja deletar novamente: " + style.WHITE)
        time.sleep(1)
        
    if decisao_deletar == "1":
        deletar_instancia(variaveis)
    elif decisao_deletar == "2":
        deletar_security_group(variaveis)
    elif decisao_deletar == "3":
        deletar_regra(variaveis)
    elif decisao_deletar == "4":
        deletar_user(aws_users)

def deletar_instancia(variaveis):
    
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    instancia_escolhida = input("Qual Instancia deseja deletar? ")
    print(style.WHITE + "Vamos deletar a Instancia " + style.RED + "{}".format(instancia_escolhida) + style.WHITE)
    escolha_deletar_instancia = input("Deseja continuar? (y/n) ")
    
    while y_ou_n(escolha_deletar_instancia):
        print(style.WHITE + "Vamos deletar a Instancia " + style.RED + "{}".format(instancia_escolhida) + style.WHITE)
        escolha_deletar_instancia = input("Deseja continuar? (y/n) ")
    if escolha_deletar_instancia == "y":
        print(style.MAGENTA + "\nDeletando Instancia..\n")
        variaveis["instances"].pop(str(instancia_escolhida))
        for chave in variaveis["security_group_instances"].copy():
            if instancia_escolhida == chave:
                del variaveis["security_group_instances"][str(instancia_escolhida)]
        escreve_variaveis(variaveis)
    elif escolha_deletar_instancia == "n":
        print(style.MAGENTA + "\nInstancia nāo deletada..\n")
        
def deletar_security_group(variaveis):
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    security_group_escolhida = input("Qual Security Group deseja deletar? ")
    print(style.WHITE + "\nVamos deletar o Security Group " + style.RED + "{}".format(security_group_escolhida) + style.WHITE)
    escolha_deletar_security_group = input("\nDeseja continuar? (y/n) ")

    while y_ou_n(escolha_deletar_security_group):
        escolha_deletar_security_group = input("\nDeseja continuar? (y/n) ")

    if escolha_deletar_security_group == "y":
        print(style.MAGENTA + "\nDeletando Security Group..\n")
        lista_security_groups = len(variaveis["security_groups"])
        for i in range(lista_security_groups):
            if variaveis["security_groups"][str(security_group_escolhida)]["name"] == security_group_escolhida:  
                variaveis["security_groups"].pop(security_group_escolhida)
                i -= 1
                escreve_variaveis(variaveis)
                break

    elif escolha_deletar_security_group == "n":
        print(style.MAGENTA + "\nSecurity Group nāo deletado..\n")
        
def deletar_regra(variaveis):
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    
    security_group_escolhida = input("Qual Security Group deseja modificar? ")
    print(style.WHITE + "Vamos modificar regras da Security Group " + style.RED 
          + "{}".format(security_group_escolhida) + style.WHITE)
    
    for i in range(len(variaveis["security_groups"][str(security_group_escolhida)]["ingress"])):
        regras = variaveis["sec_groups"][str(security_group_escolhida)]["ingress"][i]["ingress"]
        print(style.CYAN + "(0)" + style.WHITE + " {}".format(regras["description"]))
        print(style.CYAN + "(1)" + style.WHITE + " {}".format(regras["protocol"]))
        print(style.CYAN + "(2)" + style.WHITE + " {}".format(regras["from_port"]))
        print(style.CYAN + "(3)" + style.WHITE + " {}".format(regras["to_port"]))
        print(style.CYAN + "(4)" + style.WHITE + " {}".format(regras["cidr_blocks"]))
        
    regra_escolhida = input(style.CYAN + "\nQual regra deseja deletar? ")
    escolha_deletar_security_group = input("\nDeseja continuar? (y/n) ")
    while y_ou_n(escolha_deletar_security_group):
        escolha_deletar_security_group = input("Deseja continuar? (y/n) ")
    if escolha_deletar_security_group == "y":
        print("\nDeletando Regra..\n")
        variaveis["security_groups"][str(security_group_escolhida)]["ingress"].pop(int(regra_escolhida))
        escreve_variaveis(variaveis)
    elif escolha_deletar_security_group == "n":
        print(f"\nRegra de Security Group nāo deletada..\n")
    
def deletar_user(aws_users):
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    
    user_escolhido = input("Qual User deseja deletar? ")
    print(style.WHITE + "\nVamos deletar o User " + style.RED + "{}".format(user_escolhido) + style.WHITE)
    escolha_deletar_user = input("\nDeseja continuar? (y/n) ")

    while y_ou_n(escolha_deletar_user):
        escolha_deletar_user = input("\nDeseja continuar? (y/n) ")

    if escolha_deletar_user == "y":
        lista_users = len(aws_users["aws_user_name"])
        for i in range(lista_users):
            if aws_users["aws_user_name"][i]["username"] == user_escolhido:
                print(style.MAGENTA + "\nDeletando User..\n")
                aws_users["aws_user_name"].pop(i)
                lista_users -= 1
                escreve_users(aws_users)
                break
        escreve_users(aws_users)

    elif escolha_deletar_user == "n":
        print(f"\nUser nāo deletado..\n")

def listar_recuros(region):
    
    session = boto3.Session(
        aws_access_key_id = ACCESS_KEY,
        aws_secret_access_key = SECRET_KEY,
        region_name=region
    )

    ec2iam = session.client('iam')
    ec2re = session.resource('ec2')

    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print("Podemos listar os seguintes recursos:")
    print(style.CYAN + "(1)" + style.WHITE + " Instâncias")
    print(style.CYAN + "(2)" + style.WHITE + " Security Groups e Regras")
    print(style.CYAN + "(3)" + style.WHITE + " Users")
    escolha_listar = input(style.CYAN + "\nO que deseja lista?r: " + style.WHITE)

    while escolha_listar != "1" and escolha_listar !="2" and escolha_listar != "3":
        print("Podemos listar os seguintes recursos:")
        print(style.CYAN + "(1)" + style.WHITE + " Instâncias")
        print(style.CYAN + "(2)" + style.WHITE + " Security Groups e Regras")
        print(style.CYAN + "(3)" + style.WHITE + " Users")
        escolha_listar = input(style.CYAN + "\nO que deseja lista?r: " + style.WHITE)
        
    if escolha_listar == "1":
        print("\nInstancias:\n")
        for each in ec2re.instances.all():
            print(f"\nId: " + each.id + " " + 
                   "\nName: " + each.tags[0]["Value"] + " " + 
                   "\nState: " + each.state["Name"] + " " +
                   "\nType: " + each.instance_type +  
                   "\nRegion: "+  each.placement['AvailabilityZone'] + "\n " + f"")
            
    elif escolha_listar == "2":
        print("\n")
        print(f"Users: " )
        for user in ec2iam.list_users()['Users']:
            print("User: {0} \ Id: {1} \ Arn: {2}\n".format(
                user['UserName'],
                user['UserId'],
                user['Arn'],
                )
            )
    elif escolha_listar == "3":
        print("\n")
        print(f"Security Groups e Regras: " )
        for each in ec2re.security_groups.all():
            print(f"Name: " + each.group_name + "\n")
            for rule in each.ip_permissions:
                print(f"Rule: " + str(rule) + "\n")

def sobe_terraform(region):
    global arquivo
    print("\n" + style.CYAN + "*"*100 + style.WHITE + "\n")
    print("Vamos subir as mudanças no Terraform")
    arquivo = f'.auto-{region}.tfvars.json'
    os.system("cd ./aws_users && terraform init && terraform  plan && terraform apply")
    os.system(f'cd ./{region} && terraform init && terraform  plan -var-file={arquivo} && terraform apply -var-file={arquivo}')
    
    # ------------------------------------------------------------------------ FUNCOES DE USO
def carrega_variaveis():
    doc = f'{region}/.auto-{region}.tfvars.json'
    with open(doc, 'r') as json_file:
        variaveis = json.load(json_file)
    return variaveis

def carrega_users():
    file = 'aws_users/.auto.tfvars.json'
    with open(file, 'r') as json_file:
        aws_users = json.load(json_file)
    return aws_users

def escreve_variaveis(variaveis):
    doc = f'{region}/.auto-{region}.tfvars.json'
    json_object = json.dumps(variaveis, indent = 4)
    with open(doc, 'w') as outfile:
        outfile.write(json_object)

def escreve_users(aws_users):
    file = 'aws_users/.auto.tfvars.json'
    json_object = json.dumps(aws_users, indent = 4)
    with open(file, 'w') as outfile:
        outfile.write(json_object)

def y_ou_n(resposta):
    if resposta == "y"  or resposta == "n":
        return False
    else:
        print(style.RED + f"Insira a resposta corretamente\n")
        return True