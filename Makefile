# up-init  — apaga db/data e sobe com scripts em db/init/
# up-restore — apaga db/data, sobe sem init e restaura o dump mais recente em db/dumps/ (ou FILE=)
SHELL := /bin/bash
COMPOSE ?= docker compose
EXEC ?= docker exec -it
EXEC_I ?= docker exec -i
CONTAINER ?= f1_postgres
DB_USER ?= admin
DB_NAME ?= formula1_db
DUMP_DIR ?= ./db/dumps

.PHONY: up up-init up-restore up-db down _wait-db _ensure-init-dir _disable-init-dir _enable-init-dir _restore-dump

# Sobe a stack sem recriar db/data (init não roda de novo se ./db/data já existir)
up:
	$(COMPOSE) up

# Base nova via db/init/*.sql (demorado na 1ª subida)
up-init: _ensure-init-dir
	$(COMPOSE) down --remove-orphans
	sudo rm -rf ./db/data
	$(COMPOSE) up -d db
	$(MAKE) _wait-db
	$(COMPOSE) up -d

# Base nova via dump em db/dumps/ (sem rodar init)
up-restore:
	@$(MAKE) _restore-dump FILE="$(FILE)"
	$(COMPOSE) up -d

# Sobe só o Postgres em segundo plano
up-db:
	$(COMPOSE) up -d db

# Parar os containers
down:
	$(COMPOSE) down

_ensure-init-dir:
	@if [ -d db/.init.bak ]; then rm -rf db/init; mv db/.init.bak db/init; fi

_disable-init-dir: _ensure-init-dir
	@mv db/init db/.init.bak
	@mkdir -p db/init

_enable-init-dir:
	@rm -rf db/init
	@if [ -d db/.init.bak ]; then mv db/.init.bak db/init; fi

_wait-db:
	@echo "Aguardando Postgres ficar healthy..."
	@for i in $$(seq 1 120); do \
		status=$$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' $(CONTAINER) 2>/dev/null || echo missing); \
		if [ "$$status" = "healthy" ]; then echo "Postgres pronto."; exit 0; fi; \
		sleep 5; \
	done; \
	echo "Timeout aguardando $(CONTAINER)."; exit 1

_restore-dump:
	@set -euo pipefail; \
	dump="$(FILE)"; \
	if [ -z "$$dump" ]; then dump=$$(ls -t $(DUMP_DIR)/*.sql $(DUMP_DIR)/*.sql.gz 2>/dev/null | head -1 || true); fi; \
	if [ -z "$$dump" ]; then echo "Nenhum dump em $(DUMP_DIR). Use FILE=... ou rode make dump."; exit 1; fi; \
	if [ ! -f "$$dump" ]; then echo "Arquivo não encontrado: $$dump"; exit 1; fi; \
	echo "Restaurando: $$dump"; \
	$(MAKE) _disable-init-dir; \
	trap '$(MAKE) _enable-init-dir' EXIT; \
	$(COMPOSE) down --remove-orphans; \
	sudo rm -rf ./db/data; \
	$(COMPOSE) up -d db; \
	$(MAKE) _wait-db; \
	if [[ "$$dump" == *.gz ]]; then gunzip -c "$$dump" | $(EXEC_I) $(CONTAINER) psql -v ON_ERROR_STOP=1 -U $(DB_USER) -d $(DB_NAME); \
	else cat "$$dump" | $(EXEC_I) $(CONTAINER) psql -v ON_ERROR_STOP=1 -U $(DB_USER) -d $(DB_NAME); fi

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
soft-clean: _ensure-init-dir
	sudo rm -rf ./db/data && $(COMPOSE) down --remove-orphans

# Derruba a stack, remove imagens usadas pela compose e apaga ./db/data (próximo dev roda init de novo).
clean: _ensure-init-dir
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

# Restaurar dump em base já no ar (ex: make restore FILE=db/dumps/arquivo.sql)
restore:
	@test -n "$(FILE)" || { echo 'Uso: make restore FILE=db/dumps/arquivo.sql'; exit 1; }
	@test -f "$(FILE)" || { echo "Arquivo não encontrado: $(FILE)"; exit 1; }
	@if [[ "$(FILE)" == *.gz ]]; then gunzip -c "$(FILE)" | $(EXEC_I) $(CONTAINER) psql -v ON_ERROR_STOP=1 -U $(DB_USER) -d $(DB_NAME); \
	else cat "$(FILE)" | $(EXEC_I) $(CONTAINER) psql -v ON_ERROR_STOP=1 -U $(DB_USER) -d $(DB_NAME); fi

# Restaurar dump compactado .sql.gz (alias; preferir restore com FILE=*.sql.gz)
restore-gz:
	@$(MAKE) restore FILE="$(FILE)"
