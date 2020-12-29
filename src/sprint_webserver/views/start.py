"""Resource module for start resources."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import KlasserService, StartListeService

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
        "index": "G16KA1",
        "runde": "Kvartfinale 1",
        "starttid": "09:30",
        "resultat_registrert": False,
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
        startliste = await StartListeService().get_all_startlister(
            self.request.app["db"]
        )

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
                "startliste": startliste,
            },
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of athletes."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        await StartListeService().create_startliste(self.request.app["db"], body)
        return web.Response(status=201)
