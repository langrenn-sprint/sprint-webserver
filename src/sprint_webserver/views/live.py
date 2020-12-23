"""Resource module for live view."""
# import logging

from aiohttp import web
import aiohttp_jinja2


# TODO: objektet bør leses fra csv fil.
# 1. Hente opp heatlisten for gjeldende klasse
# 2. Sjekke om filter på løper er på
heatliste = [
    {
        "lopsklasse": "MJ",
        "index": "MJSA1",
        "runde": "Semifinale A - Heat 1",
        "starttid": "09:00",
        "resultat_registrert": True,
    },
    {
        "lopsklasse": "MJ",
        "index": "MJSA2",
        "runde": "Semifinale A - Heat 2",
        "starttid": "09:03",
        "resultat_registrert": True,
    },
    {
        "lopsklasse": "MJ",
        "index": "MJFA",
        "runde": "Finale A",
        "starttid": "09:20",
        "resultat_registrert": False,
    },
]

# TODO: objektet bør leses fra csv fil.
# 3. Loope gjennom alle heat
# 3a. Hente løpere i heatet (resultat hvis det finnes, hvis ikke startende)
# 3b. Bygge opp objekt med løpere i heatet - alltid minimum 6
loperliste = [
    {
        "heat": "MJSA1",
        "pos": "",
        "nr": "28",
        "navn": "Lars Michael Saab",
        "klubb": "Njård",
        "plass": "1",
        "videre_til": "FA-1",
    },
    {
        "heat": "MJSA1",
        "pos": "",
        "nr": "29",
        "navn": "Ole H",
        "klubb": "Lyn",
        "plass": "2",
        "videre_til": "FA-2",
    },
    {
        "heat": "MJSA1",
        "pos": "",
        "nr": "30",
        "navn": "Lars B",
        "klubb": "Njård",
        "plass": "3",
        "videre_til": "FA-3",
    },
    {
        "heat": "MJSA2",
        "pos": "1",
        "nr": "31",
        "navn": "Eirik",
        "klubb": "Njård",
        "plass": "1",
        "videre_til": "FA-4",
    },
    {
        "heat": "MJSA2",
        "pos": "2",
        "nr": "32",
        "navn": "Gunnar",
        "klubb": "Kjelsås",
        "plass": "2",
        "videre_til": "FA-5",
    },
    {
        "heat": "MJSA2",
        "pos": "3",
        "nr": "33",
        "navn": "Lars B",
        "klubb": "Njård",
        "plass": "3",
        "videre_til": "FA-6",
    },
]

# TODO: objektet bør leses fra csv fil.
# Deltakere er alle løpere i gjeldende klasse
deltakere = [
    {
        "nr": "28",
        "navn": "Lars Michael Saab",
        "klubb": "Njård",
        "klasse": "MJ",
    },
    {
        "nr": "29",
        "navn": "Heming H",
        "klubb": "Kjelsås",
        "klasse": "MJ",
    },
    {
        "nr": "51",
        "navn": "Stig BD",
        "klubb": "Lyn",
        "klasse": "G16",
    },
]


class Live(web.View):
    """Class representing the live view."""

    async def get(self) -> web.Response:
        """Get route function that return the live result page."""
        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
        except Exception:

            valgt_klasse = ""
        try:
            valgt_startnr = self.request.rel_url.query["startnr"]
        except Exception:
            valgt_startnr = ""

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "live.html",
            self.request,
            {
                "valgt_klasse": valgt_klasse,
                "valgt_startnr": valgt_startnr,
                "deltakere": deltakere,
                "heatliste": heatliste,
                "loperliste": loperliste,
            },
        )
