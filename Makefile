COMPOSE = docker compose
API = flask
WEB_SERVER = webserver

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	${COMPOSE} up --build

restart-api:
	$(COMPOSE) restart $(API)

logs-api:
	$(COMPOSE) logs -f $(API)

logs-webserver:
	$(COMPOSE) logs -f $(API)

shell-api:
	docker exec -it ${API} sh