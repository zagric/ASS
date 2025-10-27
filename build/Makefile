DC = docker compose
APP = docker-compose.prod.yaml
APP_DEV = docker-compose.dev.yaml

.PHONY: app-dev
app-dev:
	${DC} -f ${APP_DEV} up --build -d

.PHONY: app-dev-logs
app-dev-logs:
	${DC} -f ${APP_DEV} logs -f

.PHONY: down-dev
down-dev:
	${DC} -f ${APP_DEV} down