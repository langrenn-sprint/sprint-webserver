"""Resource module for resultat view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import KjoreplanService, KlasserService


class Kjoreplan(web.View):
    """Class representing the kjoreplan / heatliste resource."""

    async def get(self) -> web.Response:
        """Get route function that return the kjøreplan page."""
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])
        kjoreplan = await KjoreplanService().get_all_heat(self.request.app["db"])

        return await aiohttp_jinja2.render_template_async(
            "kjoreplan.html",
            self.request,
            {"klasser": klasser, "kjoreplan": kjoreplan},
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of klasses."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        result = await KjoreplanService().create_kjoreplan(self.request.app["db"], body)
        return web.Response(status=result)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
