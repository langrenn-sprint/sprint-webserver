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
% adev runserver src/sprint_excel_webserver
```
## Running the API in a wsgi-server (gunicorn)
```
% poetry shell
% gunicorn sprint_excel_webserver:create_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
```
### Teste manuelt
Enten åpne din nettleser på http://localhost:8080/

Eller via curl:
```
% curl -i http://localhost:8000/
```

Når du endrer koden i webserver.py, vil webserveren laste applikasjonen på nytt autoamtisk ved lagring.

# Referanser
Flask: https://flask.palletsprojects.com/en/1.1.x/
