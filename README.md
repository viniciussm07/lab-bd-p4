# Trabalho Final — Laboratório de Banco de Dados

Base de dados **Fórmula 1** (PostgreSQL) com dados geográficos complementares, scripts de carga em `db/init/` e aplicação web Flask.

Referência: enunciado em `ProjetoFinalEnunciado.pdf` (entrega: 17/06/2026).

## Índice

- [Estrutura do projeto](#estrutura-do-projeto)
- [Status de implementação](#status-de-implementação)
- [Requisitos](#requisitos)
  - [Funcionais (RF)](#requisitos-funcionais-rf)
  - [Não funcionais (RNF)](#requisitos-não-funcionais-rnf)
  - [Regras de negócio (RN)](#regras-de-negócio-rn)
- [Artefatos SQL por funcionalidade](#artefatos-sql-por-funcionalidade)
- [Instalação e execução](#instalação-e-execução)
- [Banco de dados](#banco-de-dados)
- [Consultas e exercícios SQL](#consultas-e-exercícios-sql)
- [Testar a API (Insomnia)](#testar-a-api-insomnia)

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
├── insomnia/                 # Coleção Insomnia para testar a API
├── db/
│   ├── init/
│   │   ├── 01_schema.sql     # Esquema relacional
│   │   ├── 02_carga.sql      # Carga idempotente dos arquivos em dados/
│   │   ├── 03_limpeza.sql    # Limpeza/normalização (T1)
│   │   ├── 04_create_and_load_users.sql  # Tabela USERS + carga inicial
│   │   ├── 05_pilotos.sql    # Funções/índices do perfil Piloto
│   │   ├── 06_escuderias.sql # Funções/procedimentos do perfil Escuderia
│   │   ├── 06_admin.sql      # Triggers, dashboard admin e relatórios admin
│   │   └── 07_create_users_log.sql       # Tabela USERS_LOG
│   ├── dumps/                # Backups .sql gerados com make dump
│   └── data/                 # Volume PostgreSQL (não versionar)
└── src/
    ├── config/
    └── app/
        ├── BD/               # DAOs (acesso ao PostgreSQL)
        │   ├── admin_dao.py
        │   ├── escuderias_dao.py
        │   ├── pilotos_dao.py
        │   └── usuarios_dao.py
        ├── controllers/
        ├── middlewares/
        ├── rotas/
        └── views/templates/
```

## Status de implementação

Legenda: **SQL** = scripts em `db/init/` · **Backend** = Flask (rotas, DAOs, controllers) · **Frontend** = templates HTML/JS

| Área | SQL | Backend | Frontend |
|------|:---:|:-------:|:--------:|
| Login / logout / auditoria | ✅ | ✅ | ✅ |
| Dashboard Piloto | ✅ | ✅ | ✅ |
| Dashboard Escuderia | ✅ | ✅ | ✅ |
| Dashboard Admin | ✅ | ✅ | ❌ |
| Tela de relatórios — Piloto | ✅ | ✅ | ✅ |
| Tela de relatórios — Escuderia | ✅ | ✅ | ✅ |
| Tela de relatórios — Admin | ✅ | ❌ | ❌ |
| Cadastrar escuderia (Admin) | ⚠️ | ❌ | ❌ |
| Cadastrar piloto — formulário (Admin) | ⚠️ | ❌ | ❌ |
| Consultar piloto por sobrenome (Escuderia) | ✅ | ✅ | ✅ |
| Inserir pilotos por arquivo (Escuderia) | ✅ | ✅ | ✅ |
| Triggers de sincronização USERS | ⚠️ | — | — |

**Resumo:** Piloto e Escuderia estão integrados (SQL → API → tela). O **dashboard Admin** tem SQL e API prontos (`admin_dao.py`, `/api/admin/*`); falta `dashboard_admin.html`. Relatórios e cadastros do Admin ainda sem backend/frontend.

Credenciais de teste (aplicação):

| Tipo | Login | Senha |
|------|-------|-------|
| Admin | `admin` | `admin` |
| Piloto | `<driver_ref>_d` (ex.: `hamilton_d`) | `<driver_ref>` |
| Escuderia | `<constructor_ref>_c` (ex.: `ferrari_c`) | `<constructor_ref>` |

## Requisitos

Cada item abaixo reflete o enunciado oficial. O status indica o que já está pronto em cada camada.

### Requisitos funcionais (RF)

| ID | Requisito | SQL | Backend | Frontend |
|----|-----------|:---:|:-------:|:--------:|
| RF-01 | **Tela de Login** — autenticação e redirecionamento ao dashboard | ✅ | ✅ | ✅ |
| RF-02 | **Tela de Dashboard (estrutura comum)** — usuário logado, dados do perfil, navegação e link para relatórios | ⚠️ | ⚠️ | ⚠️ |
| RF-03 | **Dashboard Admin** — contadores; corridas da última temporada; ranking de escuderias e pilotos por pontos | ✅ | ✅ | ❌ |
| RF-04 | **Dashboard Escuderia (funções SQL)** — vitórias, pilotos distintos, primeiro/último ano | ✅ | ✅ | ✅ |
| RF-05 | **Dashboard Piloto (funções SQL)** — anos de atividade; estatísticas por ano/circuito | ✅ | ✅ | ✅ |
| RF-06 | **Tela de Relatórios** — botões por perfil e exibição dos resultados | ⚠️ | ⚠️ | ⚠️ |
| RF-07 | **Cadastrar escuderias (Admin)** — `constructor_ref`, `name`, `country_id`, `wikipedia_url` | ⚠️ | ❌ | ❌ |
| RF-08 | **Cadastrar pilotos (Admin)** — formulário em `DRIVERS` | ⚠️ | ❌ | ❌ |
| RF-09 | **Consultar piloto por sobrenome (Escuderia)** | ✅ | ✅ | ✅ |
| RF-10 | **Inserir pilotos por arquivo (Escuderia)** | ✅ | ✅ | ✅ |
| RF-11 | **Relatório 1 (Admin)** — contagem de resultados por status | ✅ | ❌ | ❌ |
| RF-12 | **Relatório 2 (Admin)** — aeroportos próximos a cidade brasileira | ✅ | ❌ | ❌ |
| RF-13 | **Relatório 3 (Admin)** — escuderias + relatório hierárquico de corridas | ✅ | ❌ | ❌ |
| RF-14 | **Relatório 4 (Escuderia)** — pilotos e vitórias | ✅ | ✅ | ✅ |
| RF-15 | **Relatório 5 (Escuderia)** — status por escuderia | ✅ | ✅ | ✅ |
| RF-16 | **Relatório 6 (Piloto)** — pontos por ano e corridas pontuadas | ✅ | ✅ | ✅ |
| RF-17 | **Relatório 7 (Piloto)** — status nas corridas do piloto | ✅ | ✅ | ✅ |

#### Detalhamento dos RF

- **RF-01** — Implementado em `login.html`, `/api/login`, `/api/logout`, `usuarios_dao.py` e `04_create_and_load_users.sql`.
- **RF-02** — Piloto e Escuderia: dashboards completos. Admin: rota `/dashboard` ainda não renderiza template; API do dashboard disponível em `/api/admin/*`.
- **RF-03** — SQL em `06_admin.sql` (`get_db_summary`, `get_latest_season_races`, rankings via `standings`). Backend em `admin_dao.py`, `admin_controllers.py` e rotas `/api/admin/*`. Rankings usam `get_latest_*_standings_from_standings()` (pontos acumulados na última rodada), pois `results` está incompleto na temporada mais recente.
- **RF-04** — Funções em `06_escuderias.sql`; expostas via `/api/escuderia/*` e `dashboard_escuderia.html`.
- **RF-05** — Funções em `05_pilotos.sql`; expostas via `/api/piloto/*` e `dashboard_piloto.html`.
- **RF-06** — `relatorios_piloto.html` e `relatorios_escuderia.html` prontos. Falta tela de relatórios do Admin. Rota `/relatorios` não retorna template para Admin.
- **RF-07 / RF-08** — Trigger de insert em `constructors`/`drivers` cria usuário em `USERS` (`06_admin.sql`). Falta endpoint e formulário de cadastro pelo Admin.
- **RF-09 / RF-10** — Integrados no dashboard da escuderia (`consultar_piloto_por_sobrenome`, `inserir_piloto_arquivo`).
- **RF-11 a RF-13** — Funções SQL prontas em `06_admin.sql`; sem integração na aplicação.
- **RF-14 / RF-15** — Integrados em `relatorios_escuderia.html` e rotas `/api/escuderia/relatorio-*`.
- **RF-16 / RF-17** — Integrados em `relatorios_piloto.html` e rotas `/api/piloto/relatorio-*`.

### Requisitos não funcionais (RNF)

| ID | Requisito | SQL | Backend | Frontend |
|----|-----------|:---:|:-------:|:--------:|
| RNF-01 | Tabela `USERS` (`userid`, `login`, `password`, `tipo`, `id_original`) | ✅ | ✅ | — |
| RNF-02 | Senha protegida (não texto puro) | ✅ | ✅ | — |
| RNF-03 | Tabela `USERS_LOG` (login/logout) | ✅ | ✅ | — |
| RNF-04 | SQL explícito no código da aplicação | — | ✅ | — |
| RNF-05 | Índices indicados e justificados no código SQL | ✅ | — | — |
| RNF-06 | Interface em português | — | — | ✅ |

- **RNF-02** — Senhas com `pgcrypto`/`crypt` na carga (`04_create_and_load_users.sql`); verificação com `bcrypt` em `usuarios_dao.py`.
- **RNF-05** — Índices em `05_pilotos.sql`, `06_escuderias.sql` e `06_admin.sql` (com comentários de justificativa). Visões materializadas **não** foram criadas.

### Regras de negócio (RN)

| ID | Regra | SQL | Backend | Frontend |
|----|-------|:---:|:-------:|:--------:|
| RN-01 | Tipos `Admin`, `Escuderia`, `Piloto` | ✅ | ✅ | ✅ |
| RN-02 | `login` único | ✅ | ✅ | — |
| RN-03 | `id_original` referencia piloto/escuderia | ✅ | ✅ | — |
| RN-04 | Piloto só visualiza (sem alteração de dados) | ✅ | ✅ | ✅ |
| RN-05 | Usuário em `USERS` ao cadastrar escuderia/piloto (triggers) | ⚠️ | — | — |
| RN-06 | Carga inicial de usuários F1 existentes | ✅ | — | — |
| RN-07 | Login duplicado cancela inserção (via constraint/trigger) | ✅ | — | — |
| RN-08 | Sobrenome só retorna piloto que correu pela escuderia | ✅ | ✅ | ✅ |
| RN-09 | Piloto duplicado (mesmo nome/sobrenome) bloqueia inserção | ✅ | ✅ | ✅ |
| RN-10 | Escopo de acesso por tipo de usuário | ✅ | ✅ | ✅ |

- **RN-05** — Triggers de **INSERT** e **DELETE** em `06_admin.sql`. Não há trigger de **UPDATE** para sincronizar alterações em `constructors`/`drivers` (exigido parcialmente pelo enunciado).

## Artefatos SQL por funcionalidade

| Funcionalidade | Arquivo | Objetos principais |
|----------------|---------|-------------------|
| Esquema e carga | `01_schema.sql`, `02_carga.sql`, `03_limpeza.sql` | Tabelas F1 + geografia |
| Usuários | `04_create_and_load_users.sql` | `USERS`, carga admin/pilotos/escuderias |
| Dashboard Piloto | `05_pilotos.sql` | `obter_anos_atividade_piloto`, `obter_estatisticas_piloto`, índices |
| Relatórios Piloto | `05_pilotos.sql` | `relatorio_pontos_por_ano_piloto`, `relatorio_contagem_status_piloto` |
| Ações Escuderia | `06_escuderias.sql` | `consultar_piloto_por_sobrenome`, `inserir_piloto_arquivo`, etc. |
| Relatórios Escuderia | `06_escuderias.sql` | `relatorio_pilotos_vitorias`, `relatorio_contagem_status_escuderia` |
| Triggers USERS | `06_admin.sql` | `tg_sync_*_to_users`, triggers AFTER INSERT/DELETE |
| Dashboard Admin | `06_admin.sql` | `get_db_summary`, `get_latest_season_races`, `get_latest_constructor_standings_from_standings`, `get_latest_driver_standings_from_standings` |
| Relatórios Admin | `06_admin.sql` | `get_result_status_counts`, `get_airport_report_by_city`, `get_admin_report_*`, `get_report_races_by_circuit` |
| Auditoria | `07_create_users_log.sql` | `USERS_LOG` |

### Rotas da API

Autenticação via cookie `auth_token` (JWT em cookie httponly), exceto login.

| Rota | Perfil |
|------|--------|
| `POST /api/login`, `POST /api/logout` | Todos |
| `GET /api/me` | Piloto, Escuderia, Admin |
| `GET /api/piloto/anos-atividade`, `/estatisticas`, `/relatorio-pontos-ano`, `/relatorio-contagem-status` | Piloto |
| `GET /api/escuderia/vitorias`, `/quantidade-pilotos`, `/anos-atividade`, `/piloto-sobrenome`, `/relatorio-pilotos-vitorias`, `/relatorio-contagem-status` | Escuderia |
| `POST /api/escuderia/piloto-arquivo` | Escuderia |
| `GET /api/admin/resumo`, `/corridas-ultima-temporada`, `/ranking-escuderias`, `/ranking-pilotos` | Admin |
| `GET /dashboard`, `GET /relatorios`, `GET /` | Views HTML |

Coleção de testes: [`insomnia/lab-bd-p4-api.json`](insomnia/lab-bd-p4-api.json) (23 requests).

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
# Primeira vez com scripts SQL (schema + carga + limpeza + usuários + funções)
make up-init

# Primeira vez a partir de backup já gerado
make up-restore
# ou dump específico:
make up-restore FILE=db/dumps/formula1_db_20260603_191449.sql
```

A aplicação web fica em `http://localhost:3000`.

### Outros comandos úteis

```bash
make psql                              # shell interativo no Postgres
make query QUERY="SELECT COUNT(*) FROM drivers;"
make sql_file FILE=exercicios/ex01.sql # caminho dentro do container (ex.: /home/exercicios/...)
make dump                              # gera backup em db/dumps/
make soft-clean                        # apaga db/data e para containers
```

Para scripts em `db/init/` em base já em execução:

```bash
docker exec -i f1_postgres psql -U admin -d formula1_db < db/init/06_admin.sql
```

## Banco de dados

| Parâmetro | Valor |
|-----------|--------|
| Container | `f1_postgres` |
| Host (host) | `localhost` |
| Porta (host) | `5436` |
| Usuário SGBD | `admin` |
| Senha SGBD | `admin123` |
| Banco | `formula1_db` |

Conexão direta:

```bash
psql -h localhost -p 5436 -U admin -d formula1_db
# senha: admin123
```

### Scripts de inicialização (`db/init/`)

Executados **apenas** na primeira subida com `db/data` vazio (fluxo `make up-init`):

1. `01_schema.sql` — esquema relacional  
2. `02_carga.sql` — carga dos arquivos em `dados/`  
3. `03_limpeza.sql` — normalização e conferências (T1)  
4. `04_create_and_load_users.sql` — tabela e população de `USERS`  
5. `05_pilotos.sql` — funções e índices do perfil Piloto  
6. `06_escuderias.sql` — funções/procedimentos do perfil Escuderia  
7. `06_admin.sql` — triggers, dashboard e relatórios do Admin  
8. `07_create_users_log.sql` — tabela `USERS_LOG`

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

Exemplo — testar função do dashboard admin direto no banco:

```bash
make query QUERY="SELECT * FROM get_latest_constructor_standings_from_standings();"
```

## Testar a API (Insomnia)

1. Importe `insomnia/lab-bd-p4-api.json` no Insomnia.
2. Selecione o ambiente **Local** (`base_url`: `http://localhost:3000`).
3. Faça login conforme o perfil (ex.: **Login (Admin)** → `admin` / `admin`).
4. Execute as rotas da pasta correspondente (cookies são enviados automaticamente).

| Pasta | Login necessário |
|-------|------------------|
| Piloto | `hamilton_d` / `hamilton` |
| Escuderia | `ferrari_c` / `ferrari` |
| Admin (Dashboard) | `admin` / `admin` |

Upload de pilotos (Escuderia): selecione `insomnia/exemplo_pilotos.csv` no campo `file` da request **Inserir pilotos via CSV**.
