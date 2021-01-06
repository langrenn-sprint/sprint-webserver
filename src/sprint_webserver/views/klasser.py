"""Resource module for resultat view."""
import json
import logging

from aiohttp import web

from sprint_webserver.services import KlasserService


class Klasser(web.View):
    """Class representing the klasser resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all klasses."""
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])
        body = json.dumps(klasser, default=str, ensure_ascii=False)
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
        result = await KlasserService().create_klasser(self.request.app["db"], body)
        return web.Response(status=result)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented


class Klasse(web.View):
    """Class representing a single klasse resource."""

    async def get(self) -> web.Response:
        """Get route function that returns a single klasse."""
        lopsklasse = self.request.match_info["lopsklasse"]
        logging.debug(f"Got request for lopsklasse {lopsklasse}")
        klasse = await KlasserService().get_klasse_by_lopsklasse(
            self.request.app["db"], lopsklasse
        )
        logging.debug(f"Got result from db {klasse}")
        if klasse:
            body = json.dumps(klasse, default=str, ensure_ascii=False)
            return web.Response(status=200, body=body, content_type="application/json")
        raise web.HTTPNotFound
