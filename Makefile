# Sobe o Postgres; com ./db/data vazio, o entrypoint executa os *.sql em db/init/ em ordem lexicográfica (01_ … 04_).
SHELL := /bin/bash
COMPOSE ?= docker compose
EXEC ?= docker exec -it
EXEC_I ?= docker exec -i
CONTAINER ?= f1_postgres
DB_USER ?= admin
DB_NAME ?= formula1_db
DUMP_DIR ?= ./db/dumps

up:
	$(COMPOSE) up

# Parar os containers
down:
	$(COMPOSE) down

exec:


# Executar query na base (ex: make query QUERY="SELECT * FROM Airports_Audit LIMIT 5;")
query:
	$(EXEC_I) $(CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "$(QUERY)"
# Entrar no psql
psql:
	$(EXEC) $(CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)
# Executar um arquivo SQL (ex: make sql_file FILE=exercicios/ex01.sql)
sql_file:
	$(EXEC_I) $(CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -f /home/$(FILE)


# Para containers/rede e dados ./db/data (cluster Postgres).
soft-clean:
	sudo rm -rf ./db/data && $(COMPOSE) down --remove-orphans

# Derruba a stack, remove imagens usadas pela compose e apaga ./db/data (próximo dev roda init de novo).
clean:
	$(COMPOSE) down -v --rmi all --remove-orphans
	rm -rf db/data

# Dump completo da base (gera .sql no host)
dump:
	mkdir -p $(DUMP_DIR)
	$(EXEC_I) $(CONTAINER) pg_dump -U $(DB_USER) -d $(DB_NAME) > $(DUMP_DIR)/$(DB_NAME)_$$(date +%Y%m%d_%H%M%S).sql

# Dump compactado (.sql.gz)
dump-gz:
	mkdir -p $(DUMP_DIR)
	$(EXEC_I) $(CONTAINER) pg_dump -U $(DB_USER) -d $(DB_NAME) | gzip > $(DUMP_DIR)/$(DB_NAME)_$$(date +%Y%m%d_%H%M%S).sql.gz

# Restaurar dump (ex: make restore FILE=db/dumps/formula1_db_20260603_153000.sql)
restore:
	cat $(FILE) | $(EXEC_I) $(CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)