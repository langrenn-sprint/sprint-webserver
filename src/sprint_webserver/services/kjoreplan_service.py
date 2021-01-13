"""Module for kjoreplan service."""
import logging
from typing import Any, List


class KjoreplanService:
    """Class representing kjoreplan service."""

    async def get_all_heat(self, db: Any) -> List:
        """Get all heat / kjøreplan function."""
        kjoreplan = []
        cursor = db.kjoreplan_collection.find()
        for document in await cursor.to_list(length=500):
            kjoreplan.append(document)
            logging.debug(document)
        return kjoreplan

    async def get_heat_by_klasse(self, db: Any, lopsklasse: str) -> List:
        """Get all heat / kjøreplan for a given klasse."""
        kjoreplan = []
        cursor = db.kjoreplan_collection.find({"Løpsklasse": lopsklasse})
        for document in await cursor.to_list(length=500):
            kjoreplan.append(document)
            logging.debug(document)
        return kjoreplan

    async def create_kjoreplan(self, db: Any, body: Any) -> int:
        """Create kjoreplan function. After deletion of existing instances, if any."""
        returncode = 201
        collist = await db.list_collection_names()
        logging.debug(collist)
        if "kjoreplan_collection" in collist:
            returncode = 202
            result = await db.kjoreplan_collection.delete_many({})
            logging.debug(result)

        # format time
        for heat in body:
            # Format time from decimal to readable format hh:mm:ss:
            time = heat["Start"].replace(",", ".")
            heat["Start"] = _format_time(time)
            logging.info(time)
            logging.info(heat["Start"])

        result = await db.kjoreplan_collection.insert_many(body)
        logging.debug("inserted %d docs" % (len(result.inserted_ids),))
        _newvalue = {"resultat_registrert": False}
        result = await db.kjoreplan_collection.update_many({}, {"$set": _newvalue})
        logging.debug(result)
        return returncode

    async def update_registrer_resultat(self, db: Any, heat: str) -> None:
        """Create kjoreplan function."""
        _myquery = {"Index": heat}
        _newvalue = {"resultat_registrert": True}
        result = await db.kjoreplan_collection.update_one(_myquery, {"$set": _newvalue})
        logging.debug(result)

    async def get_heat_by_index(self, db: Any, index: str) -> dict:
        """Get one klass by lopsklasse function."""
        heat = await db.kjoreplan_collection.find_one({"Index": index})
        logging.debug(heat)
        return heat


def _format_time(decimal_time: str) -> str:
    """Format time from decimal to readable format hh:mm:ss."""
    sekunder = int(round(float(decimal_time) * 24 * 60 * 60, 0))
    min = divmod(sekunder, 60)
    hour = divmod(min[0], 60)
    if hour[0] < 10:
        ut_hour = "0" + str(hour[0])
    else:
        ut_hour = str(hour[0])
    if hour[1] < 10:
        ut_min = "0" + str(hour[1])
    else:
        ut_min = str(hour[1])
    if min[1] < 10:
        ut_sek = "0" + str(min[1])
    else:
        ut_sek = str(min[1])
    logging.debug("Tid: " + ut_hour + ":" + ut_min + ":" + ut_sek)

    return ut_hour + ":" + ut_min + ":" + ut_sek
