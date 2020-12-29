"""Module for deltakere service."""
import logging
from typing import Any, List


class DeltakereService:
    """Class representing deltakere service."""

    async def get_all_deltakere(self, db: Any) -> List:
        """Get all deltakere function."""
        deltakere = []
        cursor = db.deltakere_collection.find()
        for document in await cursor.to_list(length=2000):
            deltakere.append(document)
            logging.debug(document)
        return deltakere

    async def get_deltakere_by_lopsklasse(self, db: Any, lopsklasse: str) -> List:
        """Get all deltakere function."""
        deltakere = []
        cursor = db.deltakere_collection.find({"Løpsklasse": lopsklasse})
        for document in await cursor.to_list(length=100):
            deltakere.append(document)
            logging.debug(document)
        return deltakere

    async def create_deltakere(self, db: Any, body: Any) -> None:
        """Create deltakere function."""
        result = await db.deltakere_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))
