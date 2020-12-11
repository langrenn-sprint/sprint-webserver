# webserver

Her finner du en enkel webserver som generer html basert på csv-filer i test-data

## Slik går du fram for å kjøre dette lokalt

## Develop and run locally
### Requirements
- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)

### Install software:
```
% git clone https://github.com/heming-langrenn/sprint-excel.git
% cd sprint-excel/webserver
% pyenv install 3.9.0
% pyenv local 3.9.0
% pipx install poetry
% pipx install nox
% pipx inject nox nox-poetry
% poetry install
```
### Running the API locally
Start the server locally:
```
% poetry shell
% adev runserver src/webserver
```
## Running the API in a wsgi-server (gunicorn)
```
%
% poetry shell
% gunicorn webserver:create_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
```
## Running the wsgi-server in Docker
To build and run the api in a Docker container:
```
% docker build -t digdir/dcat-ap-no-validator-service:latest .
% docker run --env-file .env -p 8080:8080 -d digdir/dcat-ap-no-validator-service:latest
```
The easier way would be with docker-compose:
```
docker-compose up --build
```
## Running tests
We use [pytest](https://docs.pytest.org/en/latest/) for contract testing.

To run linters, checkers and tests:
```
% nox
```

### Teste manuelt
Enten åpne din nettleser på http://localhost:8080/

Eller via curl:
```
% curl -i http://localhost:8080/
% curl -i http://localhost:8080/bye
```

Når du endrer koden i webserver.py, vil webserveren laste applikasjonen på nytt autoamtisk ved lagring.

# Referanser
Flask: https://flask.palletsprojects.com/en/1.1.x/
