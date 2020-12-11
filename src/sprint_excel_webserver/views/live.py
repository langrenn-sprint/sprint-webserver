"""Resource module for live view."""
# import logging

from aiohttp import web

# import aiohttp_jinja2


class Live(web.View):
    """Class representing the live view."""

    async def get(self) -> web.Response:
        """Get route function."""
        return web.Response(
            text="Live! Heat: " + self.request.rel_url.query["klasse"] + ".\n"
        )
