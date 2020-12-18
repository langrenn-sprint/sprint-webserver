"""Resource module for resultat view."""
import logging

from aiohttp import web


class Klasser(web.View):
    """Class representing the klasser resource."""

    async def get(self) -> web.Response:
        """Get route function."""
        return web.Response(
            text="Resultat! Heat: " + self.request.rel_url.query["klasse"] + ".\n"
        )

    async def post(self) -> web.Response:
        """Post route function."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body}")
        return web.Response(status=201)

    async def put(self) -> web.Response:
        """Post route function."""
        return web.Response(status=204)
