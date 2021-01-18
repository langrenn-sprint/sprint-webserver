# webserver

Her finner du en enkel webserver som generer html basert på csv-filer i test-data

## Slik går du fram for å kjøre dette lokalt

## Utvikle og kjøre lokalt
### Krav til programvare
- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)

### Installere programvare:
```
% git clone https://github.com/heming-langrenn/sprint-excel.git
% cd sprint-webserver
% pyenv install 3.9.0
% pyenv local 3.9.0
% pipx install poetry
% pipx install nox
% pipx inject nox nox-poetry
% poetry install
```
## Miljøvariable
Du kan sette opp ei .env fil med miljøvariable. Eksempel:
```
HOST_PORT=8080
DB_HOST=localhost
DB_USER=<brukernavn>     # sett inn korrekt brukernavn her
DB_PASSWORD=<passord>    # sett inn korrekt passord her
DB_NAME=sprint_db
```
Denne fila _skal_ ligge i .dockerignore og .gitignore
### Kjøre webserver lokalt
Start en mongodb instans, feks i docker:
```
% docker run --rm --name my-mongo -it -p 27017:27017 mongo:latest
```
Start lokal webserver mha aiohttp-devtools(adev):
```
% source .env
% cd src && poetry run adev runserver -p 8080 sprint_webserver
```
## Running the API in a wsgi-server (gunicorn)
```
% source .env
% cd src
% poetry run gunicorn sprint_webserver:create_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
```
## Running the API in docker with docker-compose
```
% docker-compose up --build
```
### Teste manuelt
Enten åpne din nettleser på http://localhost:8080/

Eller via curl:
```
% curl -i http://localhost:8080/
```
Når du endrer koden i webserver.py, vil webserveren laste applikasjonen på nytt autoamtisk ved lagring.

# Referanser
aiohttp: https://docs.aiohttp.org/

# Datamodell
(pri 1) Lopsklasser
4 Kolonner: Klasse  Løpsklasse (nøkkel)  Rekkefølge  "Antall deltakere"

(pri 4) Kjoreplan (heat lagt ut i tid)
    5 kolonner: Lopsklasse  Heat    Index (unik nøkkel for heat)  Runde   Start

(pri 2) Startliste pr Heat
6 kolonner: Pos Nr Navn Klubb Plass "Videre til"
(pri 3) Resultatliste pr Heat

5 kolonner: Plass "Videre til" Nr Navn Klubb

(pri 5) Resultatliste pr Klasse

(pri 6) Innstillinger for renn (nøkkelparametre som navn, dato ..)
