"""Resource module for foto view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import FotoService, InnstillingerService, KlasserService


class AdminFoto(web.View):
    """Class representing the Foto admin resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all foto."""
        _lopsinfo = await InnstillingerService().get_header_footer_info(
            self.request.app["db"],
        )

        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
        except Exception:
            valgt_klasse = ""  # noqa: F841

        # hente valgte foto
        foto = []
        if valgt_klasse == "":
            foto = await FotoService().get_all_foto(self.request.app["db"])
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
            "adm_foto.html",
            self.request,
            {
                "lopsinfo": _lopsinfo,
                "valgt_klasse": valgt_klasse,
                "klasser": klasser,
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
