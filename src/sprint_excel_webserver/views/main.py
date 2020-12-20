"""Resource module for main view."""
# import logging

from aiohttp import web
import aiohttp_jinja2


# TODO: klasser objektet skal leses fra db.
klasser = [
    {"klasse": "Menn junior", "lopsklasse": "MJ", "rekkefolge": "1"},
    {"klasse": "G 16 år", "lopsklasse": "G16", "rekkefolge": "2"},
]

# TODO: objektet bør leses fra csv fil.
heatliste = [
    { "lopsklasse": "MJ", "index": "MJSA1", "runde": "Semifinale A - Heat 1", "starttid": "09:00", "resultat_registrert": True,},
    { "lopsklasse": "MJ", "index": "MJSA2", "runde": "Semifinale A - Heat 2", "starttid": "09:03", "resultat_registrert": True,},
    { "lopsklasse": "MJ", "index": "MJFA", "runde": "Finale A", "starttid": "09:20", "resultat_registrert": False,},
]


class Main(web.View):
    """Class representing the main view."""

    async def get(self) -> web.Response:
        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "index.html",
            self.request,
            {"klasser": klasser, "heatliste": heatliste},
        )
