"""Resource module for start resources."""
# import logging

from aiohttp import web

# import aiohttp_jinja2


class Start(web.View):
    """Class representing the start view."""

    async def get(self) -> web.Response:
        """Get route function."""
        return "Start! Heat: " + self.request.args.get("heat") + ".\n"
