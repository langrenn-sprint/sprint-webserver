"""Resource module for resultat view."""
import json
import logging

from aiohttp import web


class Klasser(web.View):
    """Class representing the klasser resource."""

    async def get(self) -> web.Response:
        """Get route function."""
        klasser = []
        db = self.request.app["db"]
        cursor = db.test_collection.find()
        for document in await cursor.to_list(length=100):
            klasser.append(document)
            logging.debug(document)
        body = json.dumps(klasser, default=str, ensure_ascii=False)
        logging.debug(body)
        return web.Response(
            status=200,
            body=body,
            content_type="application/json",
        )

    async def post(self) -> web.Response:
        """Post route function."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        db = self.request.app["db"]
        result = await db.test_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))
        return web.Response(status=201)

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
