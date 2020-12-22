"""Resource module for resultat view."""
# import logging

from aiohttp import web

# import aiohttp_jinja2

# TODO: objektet bør leses fra csv fil.
deltakere = [
    {
        "nr": "28",
        "navn": "Lars Michael Saab",
        "klubb": "Njård",
        "klasse": "MJ",
        "plass": "1",
    },
    {
        "nr": "29",
        "navn": "Heming H",
        "klubb": "Kjelsås",
        "klasse": "MJ",
        "plass": "2",
    },
    {
        "nr": "51",
        "navn": "Stig BD",
        "klubb": "Lyn",
        "klasse": "G16",
        "plass": "1",
    },
]


class Resultat(web.View):
    """Class representing the resultat view."""

    try:
        valgt_klasse = self.request.rel_url.query["klasse"]
    except:
        valgt_klasse = ""

    async def get(self) -> web.Response:
        """Get route function."""
        return web.Response(
            text="Resultat! Heat: " + self.request.rel_url.query["klasse"] + ".\n"
        )
