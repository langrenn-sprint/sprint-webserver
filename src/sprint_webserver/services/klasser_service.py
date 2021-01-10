"""Module for klasser service."""
import logging
from typing import Any, List


class KlasserService:
    """Class representing klasser service."""

    async def get_all_klasser(self, db: Any) -> List:
        """Get all klasser function."""
        klasser = []
        cursor = db.klasser_collection.find()
        for document in await cursor.to_list(length=100):
            klasser.append(document)
            logging.debug(document)
        return klasser

    async def create_klasser(self, db: Any, body: Any) -> int:
        """Create klasser function. After deletion of existing instances, if any."""
        returncode = 201
        collist = await db.list_collection_names()
        logging.debug(collist)
        if "klasser_collection" in collist:
            returncode = 202
            result = await db.klasser_collection.delete_many({})
            logging.debug(result)

        result = await db.klasser_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))
        return returncode

    async def get_klasse(self, db: Any, klasse: str) -> dict:
        """Get one klass by klasse function."""
        result = await db.klasser_collection.find_one({"Klasse": klasse})
        return result

    async def get_klasse_by_lopsklasse(self, db: Any, klasse: str) -> dict:
        """Get one klass by lopsklasse function."""
        result = await db.klasser_collection.find_one({"Løpsklasse": klasse})
        return result
