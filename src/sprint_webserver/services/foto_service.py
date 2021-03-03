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

    async def get_foto_by_klasse(self, db: Any, lopsklasse: str) -> List:
        """Get all heat / kjøreplan for a given klasse."""
        foto = []
        cursor = db.foto_collection.find({"Løpsklasse": lopsklasse})
        for document in await cursor.to_list(length=500):
            foto.append(document)
            logging.debug(document)
        return foto

    async def create_foto(self, db: Any, body: Any) -> int:
        """Create foto function. Delete existing foto, if any."""
        returncode = 201

        # analyze tags and link in event information
        body["Heat"] = await find_heat(db, body)
        body["Løpsklasse"] = await find_klasse(db, body)
        logging.debug(body)

        result = await db.foto_collection.insert_one(body)
        id = result.inserted_id
        logging.info(f"inserted one foto with id {id}")

        # add additional tags

        return returncode


def get_seconds_diff(time1: str, time2: str) -> int:
    """Compare time1 and time2, return time diff in min."""
    seconds_diff = 1000
    t1 = datetime.datetime.strptime("1", "%S")  # nitialize time to zero
    t2 = datetime.datetime.strptime("1", "%S")
    date_patterns = [
        "%Y:%m:%d %H:%M:%S",
        "%d.%m.%Y %H:%M:%S",
        "%Y%m%d %H:%M:%S",
    ]
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

    logging.debug(t2)
    logging.debug(t2)
    seconds_diff = int((t1 - t2).total_seconds())

    return seconds_diff


async def find_heat(db: Any, tags: dict) -> str:
    """Analyse photo tags and identify heat."""
    funnetheat = ""
    alleheat = await KjoreplanService().get_all_heat(db)
    lopsdato = await InnstillingerService().get_dato(db)
    tmplopsvarighet = await InnstillingerService().get_lopsvarighet(db)
    lopsvarighet = 0
    if tmplopsvarighet.isnumeric():
        lopsvarighet = int(tmplopsvarighet)
    logging.debug(f"lopsvarighet: {lopsvarighet}")

    for heat in alleheat:
        if tags["Filename"].find(heat["Index"]) > -1:
            funnetheat = heat["Index"]
        else:
            seconds = get_seconds_diff(tags["DateTime"], lopsdato + " " + heat["Start"])
            logging.debug(f"Diff: {seconds}")

            if tags["Location"] == "start":
                # photo taken at start
                if -60 < seconds < 30:
                    funnetheat = heat["Index"]
            elif tags["Location"] == "race":
                # photo taken during race
                if 0 < seconds < lopsvarighet:
                    funnetheat = heat["Index"]
            elif tags["Location"] == "finish":
                # photo taken at finish
                if lopsvarighet - 90 < seconds < lopsvarighet + 90:
                    funnetheat = heat["Index"]
                    logging.debug(f"Found heat: {heat}")

            logging.debug(f"Heat funnet: {funnetheat}")

    return funnetheat


async def find_klasse(db: Any, tags: dict) -> str:
    """Analyse photo tags and identify løpsklasse."""
    funnetklasse = ""
    alleklasser = await KlasserService().get_all_klasser(db)
    for klasse in alleklasser:
        logging.debug(klasse)
        if tags["Filename"].find(klasse["Løpsklasse"]) > -1:
            funnetklasse = klasse["Løpsklasse"]
            logging.debug(f"Found klasse: {funnetklasse}")
        elif tags["Heat"].find(klasse["Løpsklasse"]) > -1:
            funnetklasse = klasse["Løpsklasse"]
            logging.debug(f"Found klasse: {funnetklasse}")

    return funnetklasse
