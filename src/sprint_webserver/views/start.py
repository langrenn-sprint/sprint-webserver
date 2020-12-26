"""Resource module for start resources."""
# import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import KlasserService

klubber = ["Lyn", "Kjelsås", "Njård"]

# TODO: objektet bør leses fra csv fil.
# TODO: heatlisten skal kun inneholde heat i gjeldene klasse hvis valgt.
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
    {
        "lopsklasse": "G16",
        "index": "G16FA",
        "runde": "Finale A",
        "starttid": "09:30",
        "resultat_registrert": False,
    },
]

# TODO: objektet bør leses fra csv fil.
# TODO: loperlisten skal kun lopere i gjeldene klubb hvis valgt.
loperliste = [
    {
        "heat": "MJSA1",
        "pos": "1",
        "nr": "28",
        "navn": "Lars Michael Saab",
        "klubb": "Njård",
        "plass": "1",
        "videre_til": "FA-1",
    },
    {
        "heat": "MJSA1",
        "pos": "2",
        "nr": "29",
        "navn": "Ole H",
        "klubb": "Lyn",
        "plass": "2",
        "videre_til": "FA-2",
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


class Start(web.View):
    """Class representing the start view."""

    async def get(self) -> web.Response:
        """Get route function that return the startlister page."""
        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
        except Exception:
            valgt_klasse = ""  # noqa: F841
        try:
            valgt_klubb = self.request.rel_url.query["klubb"]
        except Exception:
            valgt_klubb = ""
        try:
            valgt_heat = self.request.rel_url.query["heat"]
        except Exception:
            valgt_heat = ""  # noqa: F841

        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "start.html",
            self.request,
            {
                "valgt_klubb": valgt_klubb,
                "valgt_klasse": valgt_klasse,
                "valgt_heat": valgt_heat,
                "klasser": klasser,
                "klubber": klubber,
                "heatliste": heatliste,
                "loperliste": loperliste,
            },
        )
