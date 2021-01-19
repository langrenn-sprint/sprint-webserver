"""Resource module for resultat view."""
import json
import logging

from aiohttp import web

from sprint_webserver.services import InnstillingerService


class Innstillinger(web.View):
    """Class representing the Innstillinger resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all klasses."""
        innstillinger = await InnstillingerService().get_all_innstillinger(
            self.request.app["db"]
        )
        body = json.dumps(innstillinger, default=str, ensure_ascii=False)
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
        result = await InnstillingerService().create_innstillinger(
            self.request.app["db"], body
        )
        return web.Response(status=result)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
