# Projeto Cloud 2022

### Aluna:

- Ellen Beatriz Shen

O projeto consiste no desenvolvimento de uma aplicação capaz de provisionar uma infraestrutura por meio de uma interface para gerenciar e administrá-la (construir, alterar e deletar recursos).

## Bibliotecas e linguagens utilizadas:


![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

## Instalação Necessária:

- Bibliotecas do Python:

```shell
pip3 install -r requirements.txt
```

- Para instalar o Terraform no MacOS, vamos utilizar o HomeBrew:

```shell
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

Para demais configurações consultar [Terraform](https://developer.hashicorp.com/terraform/downloads).

- AWS CLI

Configurando AWS para usar o Terraform. Isso deve ser feito a partir da [AWS Command Line Interface](https://aws.amazon.com/pt/cli/).

Nesse passo devem ser inseridas as IAM credentials (Access Key e Secret Access Key) para autenticar o Terraform AWS provider, por meio de variáveis de ambiente.

```shell
export AWS_ACCESS_KEY_ID= {ACCESS_KEY}

export AWS_SECRET_ACCESS_KEY= {SECRET_ACCESS_KEY}
```

**WARNING:** Nunca deixe suas credenciais públicas, faça uso de variáveis de ambiente locais e do AWS CLI.

----
```shell
terraform plan -out "tfplan.out" -var-file="my.tfvars.json"
```

```shell
terraform apply "tfplan.out"
```