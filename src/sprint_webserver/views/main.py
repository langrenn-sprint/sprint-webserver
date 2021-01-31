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
        _lopsinfo = await InnstillingerService().get_header_footer_info(
            self.request.app["db"],
        )
        logging.debug(_lopsinfo)

        return await aiohttp_jinja2.render_template_async(
            "index.html",
            self.request,
            {
                "lopsinfo": _lopsinfo,
            },
        )
