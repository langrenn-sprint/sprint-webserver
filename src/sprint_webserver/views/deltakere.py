"""Resource module for resultat view."""
import json
import logging

from aiohttp import web

from sprint_webserver.services import DeltakereService


class Deltakere(web.View):
    """Class representing the deltakere resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all deltakers."""
        deltakere = await DeltakereService().get_all_deltakere(self.request.app["db"])
        body = json.dumps(deltakere, default=str, ensure_ascii=False)
        logging.debug(body)
        return web.Response(
            status=200,
            body=body,
            content_type="application/json",
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of deltakers."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        await DeltakereService().create_deltakere(self.request.app["db"], body)
        return web.Response(status=201)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented

class Deltaker(web.View):
    """Class representing a single deltaker resource."""

    async def get(self) -> web.Response:
        """Get route function that returns a single klasse."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
