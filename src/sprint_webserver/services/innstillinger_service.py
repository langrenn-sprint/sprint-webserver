"""Module for innstillinger service."""
import logging
from typing import Any, List


class InnstillingerService:
    """Class representing innstillinger service."""

    async def get_all_innstillinger(self, db: Any) -> List:
        """Get all innstillinger function."""
        innstillinger = []
        cursor = db.innstillinger_collection.find()
        for document in await cursor.to_list(length=2000):
            innstillinger.append(document)
            logging.debug(document)
        return innstillinger

    async def get_lopsnavn(self, db: Any) -> str:
        """Get one innstilling."""
        result = await db.innstillinger_collection.find_one({"Parameter": "Løpsnavn"})
        return result["Verdi"]

    async def get_arrangor(self, db: Any) -> str:
        """Get one innstilling."""
        result = await db.innstillinger_collection.find_one({"Parameter": "Arrangør"})
        return result["Verdi"]

    async def get_dato(self, db: Any) -> str:
        """Get one innstilling."""
        result = await db.innstillinger_collection.find_one({"Parameter": "Dato"})
        return result["Verdi"]

    async def get_parameter(self, db: Any, navn: str) -> str:
        """Get one innstilling."""
        result = await db.innstillinger_collection.find_one({"Parameter": navn})
        return result["Verdi"]

    async def create_innstillinger(self, db: Any, body: Any) -> int:
        """Create innstillinger function. Delete existing innstillinger, if any."""
        returncode = 201
        collist = await db.list_collection_names()
        logging.debug(collist)
        if "innstillinger_collection" in collist:
            returncode = 202
            result = await db.innstillinger_collection.delete_many({})
            logging.debug(result)

        result = await db.innstillinger_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))
        return returncode
