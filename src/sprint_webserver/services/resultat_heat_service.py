"""Module for resultatheat service."""
import logging
from typing import Any, List


class ResultatHeatService:
    """Class representing resultatheat service."""

    async def get_all_resultatheat(self, db: Any) -> List:
        """Get all resultatheat function."""
        resultatheat = []
        cursor = db.resultatheat_collection.find()
        for document in await cursor.to_list(length=2000):
            resultatheat.append(document)
            logging.debug(document)
        return resultatheat

    async def get_resultatheat_by_klasse(self, db: Any, klasse: str) -> List:
        """Get all resultatheat function."""
        resultatheat = []
        cursor = db.resultatheat_collection.find({"Løpsklasse": klasse})
        for document in await cursor.to_list(length=1000):
            resultatheat.append(document)
            logging.debug(document)
        return resultatheat

    async def create_resultatheat(self, db: Any, body: Any) -> None:
        """Create resultatheat function."""
        result = await db.resultatheat_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))

    async def get_resultatheat_by_heat(self, db: Any, heat: str) -> List:
        """Get one resultatheat by heat function."""
        resultatheat = await db.resultatheat_collection.find({"Heat": heat})
        return resultatheat

    async def get_resultatheat_by_nr(self, db: Any, nr: str) -> List:
        """Get resultatheat by klasse function."""
        resultatheat = []
        cursor = db.resultatheat_collection.find({"Nr": nr})
        for document in await cursor.to_list(length=100):
            resultatheat.append(document)
            logging.debug(document)
        return resultatheat

    async def get_resultatheat_by_nr_and_heat(
        self, db: Any, nr: str, heat: str
    ) -> dict:
        """Get resultatheat by klasse function."""
        resultat = db.resultatheat_collection.find_one({"Nr": nr}, {"Heat": heat})
        logging.debug(resultat)
        return resultat
