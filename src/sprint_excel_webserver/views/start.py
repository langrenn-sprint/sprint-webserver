"""Resource module for start resources."""
# import logging

from aiohttp import web

# import aiohttp_jinja2


class Start(web.View):
    """Class representing the start view."""

    async def get(self) -> web.Response:
        """Get route function."""
        return web.Response(
            text="Start! Heat: " + self.request.rel_url.query["heat"] + ".\n"
        )
