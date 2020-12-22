"""Module for klasser service."""
import logging
from typing import Any, List


class KlasserService:
    """Class representing klasser service."""

    async def get_all_klasser(self, db: Any) -> List:
        """Get all klasser function."""
        klasser = []
        cursor = db.test_collection.find()
        for document in await cursor.to_list(length=100):
            klasser.append(document)
            logging.debug(document)
        return klasser

    async def create_klasser(self, db: Any, body: Any) -> None:
        """Create klasser function."""
        result = await db.test_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))

    async def get_klasse_by_lopsklasse(self, db: Any, lopsklasse: str) -> dict:
        """Get one klass by lopsklasse function."""
        klasse = await db.test_collection.find_one({"Løpsklasse": lopsklasse})
        return klasse
