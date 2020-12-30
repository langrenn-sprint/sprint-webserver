"""Module for kjoreplan service."""
import logging
from typing import Any, List


class KjoreplanService:
    """Class representing kjoreplan service."""

    async def get_all_heat(self, db: Any) -> List:
        """Get all heat / kjøreplan function."""
        kjoreplan = []
        cursor = db.kjoreplan_collection.find()
        for document in await cursor.to_list(length=100):
            kjoreplan.append(document)
            logging.debug(document)
        return kjoreplan

    async def get_heat_by_klasse(self, db: Any, lopsklasse: str) -> List:
        """Get all heat / kjøreplan for a given klasse."""
        kjoreplan = []
        cursor = db.kjoreplan_collection.find({"Løpsklasse": lopsklasse})
        for document in await cursor.to_list(length=100):
            kjoreplan.append(document)
            logging.debug(document)
        return kjoreplan

    async def create_kjoreplan(self, db: Any, body: Any) -> None:
        """Create kjoreplan function."""
        result = await db.kjoreplan_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))

    async def get_heat_by_index(self, db: Any, index: str) -> dict:
        """Get one klass by lopsklasse function."""
        heat = await db.kjoreplan_collection.find_one({"Index": index})
        return heat
