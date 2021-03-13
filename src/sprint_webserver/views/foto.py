"""Resource module for foto view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import FotoService, InnstillingerService, KlasserService

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

class Foto(web.View):
    """Class representing the Foto resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all foto."""
        _lopsinfo = await InnstillingerService().get_header_footer_info(
            self.request.app["db"],
        )

        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
        except Exception:
            valgt_klasse = ""  # noqa: F841
        try:
            valgt_klubb = self.request.rel_url.query["klubb"]
        except Exception:
            valgt_klubb = ""

        # hente valgte foto
        foto = []
        if (valgt_klasse == "") and (valgt_klubb == ""):
            foto = await FotoService().get_all_foto(self.request.app["db"])
        elif valgt_klasse == "":
            foto = await FotoService().get_foto_by_klubb(
                self.request.app["db"], valgt_klubb
            )
        else:
            foto = await FotoService().get_foto_by_klasse(
                self.request.app["db"], valgt_klasse
            )
        logging.debug(len(foto))

        # hente alle klasser
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        # ensure web safe urls
        for klasse in klasser:
            klasse["KlasseWeb"] = klasse["Klasse"].replace(" ", "%20")

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "foto.html",
            self.request,
            {
                "lopsinfo": _lopsinfo,
                "valgt_klasse": valgt_klasse,
                "valgt_klubb": valgt_klubb,
                "klasser": klasser,
                "klubber": klubber,
                "foto": foto,
            },
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of klasses."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        result = await FotoService().create_foto(self.request.app["db"], body)
        return web.Response(status=result)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
