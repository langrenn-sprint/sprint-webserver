"""Resource module for main view."""
# import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import KlasserService


# TODO: objektet bør leses fra csv fil.
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


class Main(web.View):
    """Class representing the main view."""

    async def get(self) -> web.Response:
        """Get route function."""
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        return await aiohttp_jinja2.render_template_async(
            "index.html",
            self.request,
            {"klasser": klasser, "heatliste": heatliste},
        )
