"""Resource module for live view."""
# import logging

from aiohttp import web
import aiohttp_jinja2


# TODO: objektet bør leses fra csv fil.
listetype_kvart = "Startliste"
heatliste_kvart = [
    {
        "lopsklasse": "MJ",
        "index": "MJSA1",
        "runde": "Semifinale A - Heat 1",
        "starttid": "09:00",
    },
    {
        "lopsklasse": "MJ",
        "index": "MJSA2",
        "runde": "Semifinale A - Heat 2",
        "starttid": "09:03",
    },
]

# todo - dette bør være et barn av  heat objektet og så bruke rekursiv for løkke
startliste_innl_heat = [
    {
        "pos": "1",
        "nr": "28",
        "navn": "Lars Michael Saab",
        "klubb": "Njård",
        "plass": "1",
        "videre_til": "SA1-1",
    },
    {
        "pos": "2",
        "nr": "31",
        "navn": "Eirik Bjørk Halvorsen",
        "klubb": "Kjelsås",
        "plass": "2",
        "videre_til": "Ute",
    },
]


class Live(web.View):
    """Class representing the live view."""

    async def get(self) -> web.Response:
        # TODO - må bruke klasse for å hente heatliste
        klasse = self.request.rel_url.query["klasse"]
        startnr = self.request.rel_url.query["startnr"]

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "live.html",
            self.request,
            {
                "klasse": klasse,
                "startnr": startnr,
                "listetype_kvart": listetype_kvart,
                "heatliste_kvart": heatliste_kvart,
                "startliste_innl_heat": startliste_innl_heat,
            },
        )
