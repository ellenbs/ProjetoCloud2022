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

Nesse passo devem ser inseridas as IAM credentials (Access Key e Secret Access Key) para autenticaçāo do nosso ambiente.

```shell
export AWS_ACCESS_KEY_ID= {ACCESS_KEY}

export AWS_SECRET_ACCESS_KEY= {SECRET_ACCESS_KEY}
```
:warning: Nunca deixe suas credenciais públicas, faça uso de variáveis de ambiente locais e do AWS CLI.

Também precisaremos de uma chave pública da AWS, então na aba de Key Pairs, crie um novo par de chaves e coloque nas pastas das regiões. (arquivo como "public_key")

----
## Iniciando o Projeto :grin:

Agora que temos nosso ambiente pronto, podemos clonar o repositório e começar a mexer!

```shell
git clone https://github.com/ellenbs/ProjetoCloud2022
```

A Página Principal vai te informar duas opções de região: us-east-1 (Norte da Virgínia) e us-west-2 (Norte da Califórnia). Sinta-se a vontade para escolher qualquer uma!

A próxima página terá as seguintes funcionalidades:
- Lembrando que para encontrar os ids das instâncias, podemos checar o aqruivo instances.txt na pasta de cada região

1. Criar Usuário
2. Criar Instância e Security Group
3. Iniciar Instancia
4. Parar Instancia
5. Deletar Recursos
6. Listar Instraestrutura
7. Subir Users no terraform
8. Subir mudanças no terraform
9. Sair

----
### Agora que sabemos como navegar no projeto podemos rodar:
`python main.py` ou `python3 main.py`


