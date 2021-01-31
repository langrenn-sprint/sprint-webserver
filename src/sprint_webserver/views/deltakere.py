"""Resource module for resultat view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    DeltakereService,
    InnstillingerService,
    KlasserService,
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

        _lopsinfo = await InnstillingerService().get_header_footer_info(
            self.request.app["db"],
        )
        logging.debug(_lopsinfo)

        deltakere = await DeltakereService().get_all_deltakere(self.request.app["db"])

        # get klasser
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])
        # ensure web safe urls
        for klasse in klasser:
            klasse["KlasseWeb"] = klasse["Klasse"].replace(" ", "%20")

        return await aiohttp_jinja2.render_template_async(
            "deltakere.html",
            self.request,
            {
                "lopsinfo": _lopsinfo,
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
        result = await DeltakereService().create_deltakere(self.request.app["db"], body)
        return web.Response(status=result)

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
