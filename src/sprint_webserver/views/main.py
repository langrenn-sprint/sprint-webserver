"""Resource module for main view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    InnstillingerService,
)


class Main(web.View):
    """Class representing the main view."""

    async def get(self) -> web.Response:
        """Get route function that return the index page."""
        _lopsnavn = await InnstillingerService().get_lopsnavn(
            self.request.app["db"],
        )
        _lopsdato = await InnstillingerService().get_dato(
            self.request.app["db"],
        )
        logging.debug(_lopsdato)

        return await aiohttp_jinja2.render_template_async(
            "index.html",
            self.request,
            {
                "lopsnavn": _lopsnavn,
                "lopsdato": _lopsdato,
            },
        )
