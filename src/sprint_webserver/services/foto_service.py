"""Module for foto service."""
import logging
from typing import Any, List


class FotoService:
    """Class representing foto service."""

    async def get_all_foto(self, db: Any) -> List:
        """Get all foto function."""
        foto = []
        cursor = db.foto_collection.find()
        for document in await cursor.to_list(length=2000):
            foto.append(document)
            logging.debug(document)
        return foto

    async def create_foto(self, db: Any, body: Any) -> int:
        """Create foto function. Delete existing foto, if any."""
        returncode = 201

        result = await db.foto_collection.insert_one(body)
        logging.debug(f"inserted foto {result}")
        return returncode
