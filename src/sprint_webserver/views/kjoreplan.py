"""Resource module for resultat view."""
import json
import logging

from aiohttp import web

from sprint_webserver.services import KjoreplanService


class Kjoreplan(web.View):
    """Class representing the kjoreplan / heatliste resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all klasses."""
        kjoreplan = await KjoreplanService().get_all_heat(self.request.app["db"])
        body = json.dumps(kjoreplan, default=str, ensure_ascii=False)
        logging.debug(body)
        return web.Response(
            status=200,
            body=body,
            content_type="application/json",
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of klasses."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        await KjoreplanService().create_kjoreplan(self.request.app["db"], body)
        return web.Response(status=201)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
