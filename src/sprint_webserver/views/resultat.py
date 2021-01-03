"""Resource module for resultat view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    KlasserService,
    ResultatHeatService,
    ResultatService,
)

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


class Resultat(web.View):
    """Class representing the resultat view."""

    async def get(self) -> web.Response:
        """Get route function."""
        informasjon = ""
        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
        except Exception:
            informasjon = "Velg klasse for å se resultatlister."
            valgt_klasse = ""  # noqa: F841
        try:
            valgt_klubb = self.request.rel_url.query["klubb"]
        except Exception:
            valgt_klubb = ""

        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        resultatliste = await ResultatService().get_all_resultatlister(
            self.request.app["db"],
        )

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "resultat.html",
            self.request,
            {
                "informasjon": informasjon,
                "valgt_klasse": valgt_klasse,
                "valgt_klubb": valgt_klubb,
                "klasser": klasser,
                "klubber": klubber,
                "resultatliste": resultatliste,
            },
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of athletes."""
        body = await self.request.json()
        logging.info(f"Got request-body {body} of type {type(body)}")
        await ResultatService().create_resultatliste(self.request.app["db"], body)
        return web.Response(status=201)


class ResultatHeat(web.View):
    """Class representing the resultat heat view."""

    async def post(self) -> web.Response:
        """Post route function that creates a collection of athletes."""
        body = await self.request.json()
        logging.info(f"Got request-body {body} of type {type(body)}")
        await ResultatHeatService().create_resultatheat(self.request.app["db"], body)
        return web.Response(status=201)
