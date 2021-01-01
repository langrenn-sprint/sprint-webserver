"""Resource module for resultat view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import DeltakereService, KlasserService

klubber = [
    "Bækkelaget",
    "Heming",
    "Kjelsås",
    "Koll",
    "Lillomarka",
    "Lyn",
    "Njård",
    "Rustad",
    "Røa",
    "Try",
    "Årvoll",
]


class Deltakere(web.View):
    """Class representing the deltakere resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all deltakers."""
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
        deltakere = await DeltakereService().get_all_deltakere(self.request.app["db"])

        return await aiohttp_jinja2.render_template_async(
            "deltakere.html",
            self.request,
            {
                "valgt_klubb": valgt_klubb,
                "valgt_klasse": valgt_klasse,
                "klasser": klasser,
                "klubber": klubber,
                "deltakere": deltakere,
            },
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of deltakers."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        await DeltakereService().create_deltakere(self.request.app["db"], body)
        return web.Response(status=201)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented


class Deltaker(web.View):
    """Class representing a single deltaker resource."""

    async def get(self) -> web.Response:
        """Get route function that returns a single klasse."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
