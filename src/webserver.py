from flask import Flask, render_template, request

app = Flask(__name__)

## TODO: klasser objektet bør leses fra csv fil.
klasser = [
    {
        'klasse': 'Menn junior',
        'lopsklasse': 'MJ',
        'rekkefolge': '1'
    },
    {
        'klasse': 'G 16 år',
        'lopsklasse': 'G16',
        'rekkefolge': '2'
    }
]

## TODO: kjoreplan objektet bør leses fra csv fil.
kjoreplan = [
    {
        'lopsklasse': 'MJ',
        'index': 'MJSA1',
        'runde': 'Semifinale A - Heat 1',
        'starttid': '09:00'
    },
    {
        'lopsklasse': 'MJ',
        'index': 'MJSA2',
        'runde': 'Semifinale A - Heat 2',
        'starttid': '09:03'
    }
]


@app.route("/")
def index():
    return render_template("index.html", klasser=klasser, kjoreplan=kjoreplan)

@app.route("/start")
def start():
    return "Start! Heat: " + request.args.get('heat') + ".\n"

@app.route("/resultat")
def resultat():
    return "Resultat!\n"


@app.route("/live")
def live():
    return "Live!\n"


@app.route("/bye")
def bye():
    return "Bye!\n"
