"""Resource module for main view."""
# import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import KjoreplanService, KlasserService


class Main(web.View):
    """Class representing the main view."""

    async def get(self) -> web.Response:
        """Get route function that return the main page."""
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])
        kjoreplan = await KjoreplanService().get_all_heat(self.request.app["db"])

        return await aiohttp_jinja2.render_template_async(
            "index.html",
            self.request,
            {"klasser": klasser, "kjoreplan": kjoreplan},
        )
