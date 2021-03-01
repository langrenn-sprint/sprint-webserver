"""Resource module for foto view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import FotoService, InnstillingerService


class Foto(web.View):
    """Class representing the Foto resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all foto."""
        _lopsinfo = await InnstillingerService().get_header_footer_info(
            self.request.app["db"],
        )
        foto = await FotoService().get_all_foto(self.request.app["db"])
        logging.debug(len(foto))

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "foto.html",
            self.request,
            {
                "lopsinfo": _lopsinfo,
                "foto": foto,
            },
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of klasses."""
        body = await self.request.json()
        logging.info(f"Got request-body {body} of type {type(body)}")
        result = await FotoService().create_foto(self.request.app["db"], body)
        return web.Response(status=result)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
