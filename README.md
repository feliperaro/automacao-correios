# Automação Correios

## Visão Geral

O objetivo do projeto é desenvolver um programa de RPA em Python que automatize o processo de rastreamento de pacotes no site dos Correios. 
O projeto foi configurado para ser executado após clonar o repositório, criar um ambiente virtual e instalar as dependências necessárias e executando o script (`consulta_encomenda.py`) passando o parâmetro (`codigo_encomenda`) como entrada, a saída é salva em `output/output.json` dentro do projeto. 
Além disso, logs gerados durante a execução da automação estão disponíveis em `output/logs`.

## Como Começar

Siga as etapas abaixo para configurar e executar a automação:

### Clonar o Repositório

```bash
git clone https://github.com/feliperaro/automacao-correios
cd automacao-correios
```

### Criar um Ambiente Virtual

```bash
python -m venv venv
```

### Ativar o Ambiente Virtual

- No Windows:

```bash
venv\Scripts\activate
```

- No macOS/Linux:

```bash
source venv/bin/activate
```

### Instalar as Dependências

```bash
pip install -r requirements.txt
```

## Executando a Automação

Para executar a automação, utilize o seguinte comando:

```bash
python consulta_encomenda.py codigo_encomenda
```

Substitua `codigo_encomenda` pelo valor apropriado para o seu caso de uso. 

Exemplo: 
```bash
python consulta_encomenda.py LB571181225HK
```

## Saída e Logs

A saída gerada pela automação estará disponível na pasta 'output' dentro do diretório do projeto. Além disso, os logs gerados durante a execução podem ser encontrados na pasta dedicada chamada 'logs'.


## Contribuidor

- Felipe Roque
