"""Resource module for main view."""

from aiohttp import web
import aiohttp_jinja2


class Main(web.View):
    """Class representing the main view."""

    async def get(self) -> web.Response:
        """Get route function that return the index page."""
        return await aiohttp_jinja2.render_template_async(
            "index.html",
            self.request,
            {},
        )
