"""Module for foto service."""
import datetime
import logging
from typing import Any, List

from .innstillinger_service import InnstillingerService
from .kjoreplan_service import KjoreplanService
from .klasser_service import KlasserService


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

        # analyze tags and link in event information
        body["Heat"] = await find_heat(self, db, body)
        body["Løpsklasse"] = await find_klasse(self, db, body)
        logging.debug(body)

        result = await db.foto_collection.insert_one(body)
        id = result.inserted_id
        logging.info(f"inserted one foto with id {id}")

        # add additional tags

        return returncode


def get_seconds_diff(time1: str, time2: str) -> int:
    """Compare time1 and time2, return time diff in min."""
    seconds_diff = 1000
    t1 = datetime.datetime.strptime("1", "%S")
    t2 = datetime.datetime.strptime("1", "%S")
    date_patterns = ["%Y:%m:%d %H:%M:%S", "%d.%m.%Y %H:%M:%S", "%Y%m%d %H:%M:%S"]
    for pattern in date_patterns:
        try:
            t1 = datetime.datetime.strptime(time1, pattern)
        except ValueError:
            logging.debug(f"Got error parsing time {ValueError}")
            pass
        try:
            t2 = datetime.datetime.strptime(time2, pattern)
        except ValueError:
            logging.debug(f"Got error parsing time {ValueError}")
            pass

    logging.info(t1)
    logging.info(t2)
    seconds_diff = (t1 - t2).total_seconds()

    return seconds_diff


async def find_heat(self, db: Any, tags: dict) -> str:
    """Analyse photo tags and identify løpsklasse."""
    funnetheat = ""
    position = ""
    alleheat = await KjoreplanService().get_all_heat(db)
    lopsdato = await InnstillingerService().get_dato(db)

    for heat in alleheat:
        if tags["Filename"].find(heat["Index"]) > -1:
            funnetheat = heat["Index"]
        else:
            seconds = get_seconds_diff(
                tags["DateTime"], lopsdato + " " + heat["Start"]
            )
            logging.info(f"Diff: {seconds}")

            if tags["Location"] == "start":
                #photo taken at start
                if -60 < seconds < 30:
                    funnetheat = heat["Index"]
            elif tags["Location"] == "race":
                #photo taken during race
                if 0 < seconds < 180:
                    funnetheat = heat["Index"]
            elif tags["Location"] == "finish":
                #photo taken at finish
                if 80 < seconds < 240:
                    funnetheat = heat["Index"]

            logging.info(f"Heat funnet: {funnetheat}")

    return funnetheat


async def find_klasse(self, db: Any, tags: dict) -> str:
    """Analyse photo tags and identify løpsklasse."""
    funnetklasse = ""
    alleklasser = await KlasserService().get_all_klasser(db)
    for klasse in alleklasser:
        if tags["Filename"].find(klasse["Løpsklasse"]) > -1:
            funnetklasse = klasse["Løpsklasse"]
            logging.debug(funnetklasse)

    return funnetklasse
