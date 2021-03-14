"""Module for foto service."""
import datetime
import logging
from typing import Any, List

from .innstillinger_service import InnstillingerService
from .kjoreplan_service import KjoreplanService
from .klasser_service import KlasserService
from .start_service import StartListeService


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
        """Get all foto for a given klasse."""
        foto = []
        cursor = db.foto_collection.find({"Løpsklasse": lopsklasse})
        for document in await cursor.to_list(length=500):
            foto.append(document)
            logging.debug(document)
        return foto

    async def get_foto_by_klubb(self, db: Any, klubb: str) -> List:
        """Get all foto for a given klubb."""
        foto = []
        myquery = ".*" + klubb + ".*"
        cursor = db.foto_collection.find({"Klubb": {"$regex": myquery}})
        for document in await cursor.to_list(length=500):
            foto.append(document)
            logging.debug(document)
        return foto

    async def create_foto(self, db: Any, body: Any) -> int:
        """Create foto function. Delete existing foto, if any."""
        returncode = 201

        # analyze tags and link in event information
        tags_fromnumbers = await find_startnummer(db, body)
        body.update(tags_fromnumbers)
        if "Heat" not in body.keys():
            body["Heat"] = await find_heat(db, body)
        if "Løpsklasse" not in body.keys():
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


async def find_startnummer(db: Any, tags: dict) -> dict:
    """Analyse photo tags and identify startnummer."""
    nye_tags = {}
    funnetstartnummer = ""
    funnetklubber = ""
    nummere = tags["Numbers"]
    personer = tags["Persons"]
    if personer.isnumeric():
        if int(personer) > 0:
            nummerliste = nummere.split(";")
            for nummer in nummerliste:
                starter = await StartListeService().get_startliste_by_nr(db, nummer)
                if len(starter) > 0:
                    funnetstartnummer = funnetstartnummer + nummer + ";"
                    # try to identify more information
                    for start in starter:
                        logging.debug(f"Start funnet: {start}")
                        nye_tags["Løpsklasse"] = start["Løpsklasse"]
                        if start["Klubb"] not in funnetklubber:
                            funnetklubber = funnetklubber + start["Klubb"] + ";"
                        # TODO - check time to identify heat
            nye_tags["Startnummer"] = funnetstartnummer
            nye_tags["Klubb"] = funnetklubber

    return nye_tags


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

            datetime = tags.get("DateTime")
            location = tags.get("Location")
            seconds = 1000
            if not datetime == None:
                seconds = get_seconds_diff(datetime, lopsdato + " " + heat["Start"])
            logging.debug(f"Diff: {seconds}")

            if location == "start":
                # photo taken at start
                if -60 < seconds < 30:
                    funnetheat = heat["Index"]
            elif location == "race":
                # photo taken during race
                if 0 < seconds < lopsvarighet:
                    funnetheat = heat["Index"]
            elif location == "finish":
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

    return funnetklasse
