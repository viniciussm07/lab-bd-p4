# Trabalho Final — Laboratório de Banco de Dados

Base de dados **Fórmula 1** (PostgreSQL) com dados geográficos complementares, scripts de carga em `db/init/` e aplicação web Flask 


## Índice

- [Estrutura do projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
  - [Funcionais (RF)](#requisitos-funcionais-rf)
  - [Não funcionais (RNF)](#requisitos-não-funcionais-rnf)
  - [Regras de negócio (RN)](#regras-de-negócio-rn)
- [Instalação e execução](#instalação-e-execução)
- [Banco de dados](#banco-de-dados)
- [Consultas e exercícios SQL](#consultas-e-exercícios-sql)

## Estrutura do projeto

```
lab-bd-p4/
├── server.py                 # Entrada da aplicação Flask
├── requirements.txt
├── Dockerfile
├── docker-compose.yml        # Postgres (formula1_db) + web
├── Makefile                  # up-init, up-restore, dump, psql, etc.
├── dados/                    # CSV/TSV de carga (F1 + geografia)
├── exercicios/               # SQL dos exercícios (montado no container em /home/exercicios)
├── db/
│   ├── init/
│   │   ├── 01_schema.sql     # Esquema relacional
│   │   ├── 02_carga.sql      # Carga idempotente dos arquivos em dados/
│   │   └── 03_limpeza.sql    # Limpeza/normalização (T1)
│   ├── dumps/                # Backups .sql gerados com make dump
│   └── data/                 # Volume PostgreSQL (não versionar)
└── src/
    ├── config/
    └── app/                  # Controllers, DAOs, templates
```

## Requisitos

### Requisitos funcionais (RF)

- [ ] **RF-01** — **Tela de Login**
  Tela 1: solicita a identificação do usuário e sua senha. Após a confirmação do login, deve ser apresentada a Tela 2.

- [ ] **RF-02** — **Tela de Dashboard**  
  Tela 2: apresenta informações sumarizadas de acordo com o tipo de usuário logado e deve funcionar como a tela principal de navegação da ferramenta. Em todas as variações, deve apresentar:
  - o nome ou identificação do usuário logado;
  - as informações de dashboard correspondentes ao tipo de usuário;
  - botões ou links para as ações disponíveis ao tipo de usuário autenticado;
  - caminho para a Tela 3, destinada aos relatórios.

- [ ] **RF-03** — **Dashboard do Administrador**  
  Painel do usuário `Admin`. A tela deve:
  - mostrar quem é o usuário logado e destacar que ele tem privilégio de administrador;
  - exibir contadores do banco: total de pilotos, escuderias e temporadas cadastrados;
  - listar as corridas da temporada mais recente, com circuito, data, horário e quantidade de voltas registrada nos resultados.

- [ ] **RF-04** — **Consulta de escuderia (funções/procedimentos)**  
  Escuderia: nome da escuderia e quantidade de pilotos associados a ela. Devem ser criadas funções ou procedimentos armazenados que recebam dados da escuderia como parâmetro e retornem: (1) quantidade de vitórias da escuderia, considerando as corridas em que obteve a primeira posição; (2) quantidade de pilotos diferentes que já correram pela escuderia; (3) primeiro e último ano em que há dados da escuderia na base, considerando a tabela `RESULTS`.

- [ ] **RF-05** — **Consulta de piloto (funções/procedimentos)**  
  Piloto: nome da escuderia associada e nome completo do piloto. Devem ser criadas funções ou procedimentos armazenados que recebam dados do piloto como parâmetro e retornem: (1) primeiro e último ano em que há dados do piloto na base, considerando a tabela `RESULTS`; (2) para cada ano em que o piloto competiu e para cada circuito em que correu: quantidade de pontos obtidos; quantidade de vitórias (corridas em 1ª posição); quantidade total de corridas em que participou.

- [ ] **RF-06** — **Tela de Relatórios**  
  Tela 3: deve apresentar botões ou recursos equivalentes para solicitar os relatórios disponíveis ao tipo de usuário logado. Sempre que um relatório for solicitado, a tela deve apresentar o resultado correspondente. Após o encerramento da visualização de um relatório, a ferramenta deve retornar à Tela 3.

- [ ] **RF-07** — **Cadastrar escuderias**  
  Formulário para nova tupla em `CONSTRUCTORS`: `constructor_ref`, `name`, `country_id`, `wikipedia_url`.

- [ ] **RF-07 (pilotos)** — **Cadastrar pilotos**  
  Formulário para novo piloto em `DRIVERS`: `driver_ref`, `given_name`, `family_name`, `date_of_birth`, `country_id`.

- [ ] **RF-08** — **Cadastrar pilotos**  
  Exibe uma janela ou formulário para inserir um novo piloto na tabela `DRIVERS`. Campos: `driver_ref`, `given_name`, `family_name`, `date_of_birth`, `country_id`.

- [ ] **RF-09** — **Consultar piloto por sobrenome**  
  Exibe formulário para indicar o sobrenome de um piloto. O programa deve verificar se há piloto com esse sobrenome que já tenha corrido pela escuderia logada. Caso exista, apresentar nome completo, data de nascimento e país/nacionalidade associada.

- [ ] **RF-10** — **Inserir pilotos por arquivo**  
  Exibe formulário para indicar arquivo acessível no SO com um ou mais pilotos (uma linha por piloto). Cada linha deve conter: `driver_ref`, `given_name`, `family_name`, `date_of_birth`, `country_id`.

- [ ] **RF-11** — **Relatório 1**  
  Indica a quantidade de resultados por status, apresentando o nome do status e sua respectiva contagem.

- [ ] **RF-12** — **Relatório 2**  
  Recebe o nome de uma cidade e, para cada cidade brasileira com esse nome, apresenta aeroportos brasileiros a no máximo 100 km, dos tipos `medium_airport` ou `large_airport`. Colunas: nome da cidade pesquisada; código IATA; nome do aeroporto; cidade do aeroporto; distância; tipo do aeroporto.

- [ ] **RF-13** — **Relatório 3**  
  Lista escuderias com quantidade de pilotos e gera relatório hierárquico em três níveis: (1) total de corridas cadastradas; (2) corridas por circuito, com mínimo, média e máximo de voltas nos resultados; (3) por corrida/circuito, voltas registradas e pilotos participantes.

- [ ] **RF-14** — **Relatório 4**  
  Lista os pilotos da escuderia e quantas vezes cada um alcançou a 1ª posição em uma corrida. Pilotos identificados pelo nome completo.

- [ ] **RF-15** — **Relatório 5**  
  Lista a quantidade de resultados por status (status e contagem), limitada ao escopo da escuderia logada.

- [ ] **RF-16** — **Relatório 6**  
  Consulta a quantidade total de pontos obtidos por ano de participação na Fórmula 1, apresentando, para cada ano, as corridas em que os pontos foram obtidos. Restrito ao piloto logado.

- [ ] **RF-17** — **Relatório 7**  
  Lista a quantidade de resultados por status nas corridas em que o piloto participou (status e contagem), limitado ao escopo do piloto logado.

### Requisitos não funcionais (RNF)

- [ ] **RNF-01** — **Tabela USERS**  
  Criar tabela `USERS` com no mínimo: `userid`, `login`, `password`, `tipo`, `id_original`.

- [ ] **RNF-02** — **Senha protegida**  
  A senha dos usuários deve ser armazenada de forma protegida. Se a implementação usar usuários reais do PostgreSQL, a autenticação deve usar SCRAM-SHA-256. Se a autenticação for pela tabela `USERS`, não armazenar senha em texto puro.

- [ ] **RNF-03** — **Auditoria de acesso**  
  Criar tabela `USERS_LOG` para auditar login e logout. Cada registro deve conter, no mínimo: `userid`; tipo da ação (`LOGIN` / `LOGOUT`); data e hora da ação.

- [ ] **RNF-04** — **SQL explícito no código**  
  Os comandos SQL usados pela aplicação devem estar explícitos no código. Não usar ferramentas que automatizem ou ocultem os scripts executados, impedindo análise na avaliação.

- [ ] **RNF-05** — **Índices justificados**  
  Os índices criados para auxiliar os relatórios devem ser indicados no código e justificados brevemente no relatório final, explicando quais filtros, junções ou ordenações eles procuram otimizar.

- [ ] **RNF-06** — **Interface em português**  
  As informações devem ser apresentadas de forma intuitiva. Nomes de colunas em telas, tabelas, dashboards e relatórios devem estar inteligíveis em Língua Portuguesa.

### Regras de negócio (RN)

- [ ] **RN-01** — **Tipos de usuário**  
  Cada usuário deve pertencer a apenas um dos tipos: `Admin`, `Escuderia` ou `Piloto`.

- [ ] **RN-02** — **Login único**  
  O atributo `login` deve ser único.

- [ ] **RN-03** — **Identificador de origem**  
  O atributo `id_original` deve armazenar o identificador do registro correspondente na tabela de origem (piloto ou escuderia).

- [ ] **RN-04** — **Restrição do piloto**  
  Usuários do tipo `Piloto` não podem alterar dados da base; apenas visualizar relatórios e dashboard referentes ao próprio piloto.

- [ ] **RN-05** — **Usuário automático no cadastro**  
  Ao cadastrar escuderia ou piloto, inserir automaticamente o respectivo usuário em `USERS` via triggers, seguindo os padrões de login e senha definidos.

- [ ] **RN-06** — **Carga inicial de usuários**  
  Pilotos e escuderias já existentes na base F1 devem ser cadastrados em `USERS`, seguindo os padrões de login e senha definidos.

- [ ] **RN-07** — **Unicidade de login (trigger)**  
  Se já existir usuário com o login gerado, a trigger deve cancelar a operação e impedir inserção inconsistente na tabela de origem.

- [ ] **RN-08** — **Piloto já vinculado à escuderia**  
  O programa deve verificar se há piloto com o sobrenome informado que já tenha corrido pela escuderia logada. Dica: consultar a tabela `RESULTS`.

- [ ] **RN-09** — **Piloto duplicado**  
  Antes da inserção, verificar que não exista outro piloto com o mesmo nome e sobrenome. Se já existir, informar o usuário e cancelar a inserção.

- [ ] **RN-10** — **Escopo de acesso por tipo**  
  **Escuderia:** acessa somente informações da própria escuderia e dos pilotos que correm ou correram por ela. **Piloto:** acessa somente informações do próprio desempenho.

## Instalação e execução

### Requisitos de software

- Docker 20.10+
- Docker Compose v2
- Make 4+ (opcional, recomendado)

```bash
docker --version
docker compose version
make --version
```

### Subir o ambiente

| Comando | Quando usar |
|---------|-------------|
| `make up-init` | Base **nova** via scripts `db/init/` (carga completa; demorado na 1ª vez) |
| `make up-restore` | Base **nova** a partir do dump mais recente em `db/dumps/` (sem rodar init) |
| `make up` | Sobe a stack **sem apagar** `db/data` (init não repete se o volume já existir) |
| `make down` | Para os containers |

Exemplos:

```bash
# Primeira vez com scripts SQL (schema + carga + limpeza)
make up-init

# Primeira vez a partir de backup já gerado
make up-restore
# ou dump específico:
make up-restore FILE=db/dumps/formula1_db_20260603_191449.sql
```

A aplicação web (quando configurada) fica em `http://localhost:3000`.

### Outros comandos úteis

```bash
make psql                              # shell interativo no Postgres
make query QUERY="SELECT COUNT(*) FROM drivers;"
make sql_file FILE=exercicios/ex01.sql # arquivo em ./exercicios → /home/exercicios no container
make dump                              # gera backup em db/dumps/
make soft-clean                        # apaga db/data e para containers
```

## Banco de dados

| Parâmetro | Valor |
|-----------|--------|
| Container | `f1_postgres` |
| Host (host) | `localhost` |
| Porta (host) | `5436` |
| Usuário | `admin` |
| Senha | `admin123` |
| Banco | `formula1_db` |

Conexão direta:

```bash
psql -h localhost -p 5436 -U admin -d formula1_db
# senha: admin123
```

### Scripts de inicialização (`db/init/`)

Executados **apenas** na primeira subida com `db/data` vazio (fluxo `make up-init`):

1. `01_schema.sql` — cria tabelas F1 e geográficas  
2. `02_carga.sql` — carrega arquivos de `dados/`  
3. `03_limpeza.sql` — normalização e conferências (T1)

### Reiniciar do zero

```bash
make soft-clean
make up-init    # ou make up-restore
```

## Consultas e exercícios SQL

Arquivos em `exercicios/` são montados em `/home/exercicios` no container:

```bash
make sql_file FILE=exercicios/seu_arquivo.sql
```
