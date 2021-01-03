"""Module for startliste service."""
import logging
from typing import Any, List


class StartListeService:
    """Class representing startliste service."""

    async def get_all_startlister(self, db: Any) -> List:
        """Get all startlister function."""
        startlister = []
        cursor = db.startliste_collection.find()
        for document in await cursor.to_list(length=2000):
            startlister.append(document)
            logging.debug(document)
        return startlister

    async def get_startliste_by_klasse(self, db: Any, klasse: str) -> List:
        """Get all startlister function."""
        startlister = []
        cursor = db.startliste_collection.find({"Løpsklasse": klasse})
        for document in await cursor.to_list(length=1000):
            startlister.append(document)
            logging.debug(document)
        return startlister

    async def create_startliste(self, db: Any, body: Any) -> None:
        """Create startlister function."""
        result = await db.startliste_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))

    async def get_startliste_by_heat(self, db: Any, heat: str) -> dict:
        """Get one startliste by heat function."""
        startliste = await db.startliste_collection.find({"Heat": heat})
        return startliste

    async def get_startliste_by_nr(self, db: Any, nr: str) -> List:
        """Get startlister by klasse function."""
        startlister = []
        cursor = db.startliste_collection.find({"Nr": nr})
        for document in await cursor.to_list(length=100):
            startlister.append(document)
            logging.debug(document)
        return startlister
