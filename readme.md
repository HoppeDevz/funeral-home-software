# 💀 Sistema para Funerária – Estrutura de Dados

## 🧩 Entidades

### Titular
- id
- nome
- data_nascimento
- estado_civil
- cpf
- rg
- endereco
- bairro
- cep
- cidade
- telefone

### Dependente
- id
- id_titular (FK)
- nome

### Plano
> Representa o modelo genérico de um plano oferecido pela funerária.
- id
- nome
- preco_mensalidade
- quantidade_parcelas

### Contrato
> Representa a contratação de um plano por um titular.
- id
- id_titular (FK)
- id_plano (FK)
- dia_pagamento
- data_criacao
- parcelas_pagas (int)

### UsoContratoTitular
- id
- id_titular (FK)
- id_contrato (FK)
- data_uso

### UsoContratoDependente
- id
- id_dependente (FK)
- id_contrato (FK)
- data_uso

---

## 🔗 Relações

- Um **Titular** possui vários **Dependentes**
- Um **Titular** pode ter vários **Contratos**
- Um **Contrato** se refere a um único **Plano**
- Um **Contrato** pode ser usado pelo **Titular** ou seus **Dependentes**

---

## ⚙️ Operações do Sistema

### Criação
- Criar **Titular**
- Criar **Dependente** (vinculado a um Titular)
- Criar **Plano** (modelo de plano com nome e preço)
- Criar **Contrato** (vinculado a um Titular e a um Plano)

### Listagem
- **Listar Titulares** (com filtro por nome)
- **Listar Dependentes** de um titular:
  - Mostrar nome

- **Listar Contratos** de um titular, com:
  - Nome do plano
  - Preço da mensalidade
  - Dia do pagamento
  - Data de criação
  - Parcelas pagas
  - Se foi usado
  - Quem usou:
    - Nome do usuário
    - Tipo: Titular ou Dependente
    - Data do uso

### Pagamento
- **Dar baixa** em um contrato:
  - Informar quantas parcelas foram pagas
  - Somar ao campo parcelas_pagas

### Uso
- Registrar **uso do contrato por Titular**
- Registrar **uso do contrato por Dependente**

------------------------------------------------------------------
--------------------- 🔹 [1] Criar novo titular -------------------
------------------------------------------------------------------
➡️ Nome completo: João Carlos Mendes  
➡️ Data de nascimento (dd/mm/aaaa): 12/05/1970  
➡️ Estado civil (Solteiro, Casado, etc.): Casado  
➡️ CPF (somente números): 12345678901  
➡️ RG: MG1234567  
➡️ Endereço (rua, número): Rua das Acácias, 123  
➡️ Bairro: Centro  
➡️ CEP: 30123-000  
➡️ Cidade: Belo Horizonte  
➡️ Telefone (opcional): (31) 91234-5678

📋 Confirmar os dados abaixo:

Nome: João Carlos Mendes  
Data de nascimento: 12/05/1970  
Estado civil: Casado  
CPF: 123.456.789-01  
RG: MG1234567  
Endereço: Rua das Acácias, 123 – Centro – Belo Horizonte – 30123-000  
Telefone: (31) 91234-5678

➡️ Confirmar cadastro? (s/n): s

✔️ Titular cadastrado com sucesso! ID: 12  
------------------------------------------------------------------

------------------------------------------------------------------
-------------------- 🔹 [2] Criar dependente ----------------------
------------------------------------------------------------------
➡️ Digite o nome (ou parte do nome) do titular: joao

📋 Titulares encontrados:
[12] João Carlos Mendes

➡️ Digite o ID do titular: 12

➡️ Nome completo do dependente: Ana Mendes

✔️ Dependente "Ana Mendes" vinculado ao titular João Carlos Mendes cadastrado com sucesso! ID: 3  
------------------------------------------------------------------

------------------------------------------------------------------
----------------------- 🔹 [3] Criar plano ------------------------
------------------------------------------------------------------
➡️ Nome do plano: Plano Ouro  
➡️ Preço da mensalidade (R$): 89.90  
➡️ Quantidade de parcelas: 12

✔️ Plano "Plano Ouro" cadastrado com sucesso! ID: 2  
------------------------------------------------------------------

------------------------------------------------------------------
---------------------- 🔹 [4] Criar contrato ----------------------
------------------------------------------------------------------
➡️ Digite o nome (ou parte do nome) do titular: joao

📋 Titulares encontrados:
[12] João Carlos Mendes

➡️ Digite o ID do titular: 12

📋 Planos disponíveis:
[2] Plano Ouro - R$ 89,90

➡️ Digite o ID do plano: 2  
➡️ Dia do pagamento (1-31): 10  
➡️ Data de criação (dd/mm/aaaa): 01/06/2025  
➡️ Parcelas pagas (inicialmente 0): 0

✔️ Contrato do plano "Plano Ouro" vinculado ao titular João Carlos Mendes cadastrado com sucesso! ID: 5  
------------------------------------------------------------------

------------------------------------------------------------------
-------------------- 🔹 [5] Listar titulares ---------------------
------------------------------------------------------------------
➡️ Digite o nome (ou parte do nome) do titular: joao

📋 Titulares encontrados:

Nome: João Carlos Mendes  
Data de nascimento: 12/05/1970  
Estado civil: Casado  
CPF: 123.456.789-01  
RG: MG1234567  
Endereço: Rua das Acácias, 123 – Centro – Belo Horizonte – 30123-000  
Telefone: (31) 91234-5678

Nome: João Pedro Silva  
Data de nascimento: 26/03/1980  
Estado civil: Casado  
CPF: 123.456.789-01  
RG: MG1234567  
Endereço: Rua das Acácias, 123 – Centro – Belo Horizonte – 30123-000  
Telefone: (31) 91234-5678

------------------------------------------------------------------

------------------------------------------------------------------
------------ 🔹 [6] Listar dependentes de um titular -------------
------------------------------------------------------------------
➡️ Digite o nome (ou parte do nome) do titular: roberto

📋 Titulares encontrados:
[5] Roberto Lima
[6] Roberto Teixeira

➡️ Digite o ID do titular: 5

👨‍👧 Dependentes de Roberto Lima:
[1] Carlos Lima
[2] Fernanda Lima
------------------------------------------------------------------

------------------------------------------------------------------
-------------- 🔹 [7] Listar contratos de um titular --------------
------------------------------------------------------------------
➡️ Digite o nome (ou parte do nome) do titular: roberto

📋 Titulares encontrados:
[5] Roberto Lima  
[6] Roberto Teixeira

➡️ Digite o ID do titular: 5

📄 Contratos de Roberto Lima:
[1] Plano: Plano Ouro - R$ 89,90  
    Dia do pagamento: 10  
    Data de criação: 01/01/2024  
    Parcelas pagas: 6 / Quantidade de parcelas: 12  
    Foi usado: Sim  
    Usuários que usaram:
      - Titular (10/02/2024)
      - Ana Lima (dependente) (15/03/2024)

[2] Plano: Plano Básico - R$ 49,90  
    Dia do pagamento: 05  
    Data de criação: 15/03/2024  
    Parcelas pagas: 2 / Quantidade de parcelas: 6  
    Foi usado: Não
------------------------------------------------------------------

------------------------------------------------------------------
------------ 🔹 [8] Dar baixa em parcelas de um contrato ----------
------------------------------------------------------------------
➡️ Digite o nome (ou parte do nome) do titular: joao

📋 Titulares encontrados:
[1] João da Silva  
[2] João Pedro Andrade

➡️ Digite o ID do titular: 1

📄 Contratos do titular:
[1] Plano: Plano Ouro - R$ 89,90 - 6 parcelas pagas  
[2] Plano: Plano Básico - R$ 49,90 - 2 parcelas pagas

➡️ Digite o ID do contrato: 2

✅ Parcelas pagas: 2

➡️ Quantas parcelas deseja adicionar? 1

✔️ Parcelas atualizadas com sucesso.  
✔️ Total agora: 3 parcelas pagas.
------------------------------------------------------------------

------------------------------------------------------------------
---------- 🔹 [9] Registrar uso de contrato por dependente --------
------------------------------------------------------------------
➡️ Digite o nome (ou parte do nome) do titular: maria

📋 Titulares encontrados:
[3] Maria de Souza

➡️ Digite o ID do titular: 3

👨‍👧 Dependentes:
[1] Pedro Souza  
[2] Ana Souza

➡️ Digite o ID do dependente: 2

📄 Contratos do titular:
[1] Plano: Plano Prata  
[2] Plano: Plano Familiar

➡️ Digite o ID do contrato: 2

📅 Data do uso (dd/mm/aaaa): 10/06/2025

✔️ Uso registrado com sucesso.
------------------------------------------------------------------

------------------------------------------------------------------
----------- 🔹 [10] Registrar uso de contrato por titular ----------
------------------------------------------------------------------
➡️ Digite o nome (ou parte do nome) do titular: maria

📋 Titulares encontrados:
[3] Maria de Souza

➡️ Digite o ID do titular: 3

📄 Contratos do titular:
[1] Plano: Plano Prata  
[2] Plano: Plano Familiar

➡️ Digite o ID do contrato: 2

📅 Data do uso (dd/mm/aaaa): 10/06/2025

✔️ Uso registrado com sucesso.
------------------------------------------------------------------

tudo certo agora?


