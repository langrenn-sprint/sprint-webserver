# webserver

Her finner du en enkel webserver som generer html basert på csv-filer i test-data

## Slik går du fram for å kjøre dette lokalt

### Lag virtuelt miljø og installer Flask
Følgende instruksjoner er tilpassa til linux, men vil med enkle justeringer fungere både på Windows og Mac
```
% python3 -m venv venv
% . venv/bin/activate
% pip install Flask
```
### Start webserver
```
% FLASK_APP=src/webserver.py  FLASK_ENV=development flask run --port=8080
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
