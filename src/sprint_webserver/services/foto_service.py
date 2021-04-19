"""Module for foto service."""
import datetime
import logging
from typing import Any, List

from .deltakere_service import DeltakereService
from .innstillinger_service import InnstillingerService
from .kjoreplan_service import KjoreplanService
from .klasser_service import KlasserService
from .start_service import StartListeService

klubber = [
    "Bækkelaget",
    "Heming",
    "Kjelsås",
    "Koll",
    "Lillomarka",
    "Lyn",
    "Njård",
    "Rustad",
    "Røa",
    "Try",
    "Årvoll",
]


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

        # analyze tags and enrich with event information
        tags_fromnumbers = await find_event_information(db, body)
        body.update(tags_fromnumbers)
        if "Løpsklasse" not in body.keys():
            body["Løpsklasse"] = await find_lopsklasse(db, body)
        logging.debug(body)

        result = await db.foto_collection.insert_one(body)
        logging.info(f"inserted one foto with id {result.inserted_id}")

        return returncode

    async def update_tags(self, db: Any, tags: Any) -> None:
        """Update tags for one photo."""
        logging.debug(f"Got tags {tags} of type {type(tags)}")

        newvalues = {}
        for x, y in tags.items():
            if x == "OldNumbers":
                oldnumbers = y
            elif x == "Filename":
                myquery = {"Filename": y}

            else:
                newvalues[x] = y

        # enrich data
        nummere = tags["Numbers"]
        if oldnumbers != nummere:
            nummerliste = nummere.split(";")
            for nummer in nummerliste:
                tmp_tags = await find_info_from_startnummer(
                    db, nummer, tags["DateTime"]
                )
                for x, y in tmp_tags.items():
                    logging.debug(f"Found tag: {x}, {y}")
                    if x not in newvalues.keys():
                        newvalues[x] = y
                    elif newvalues[x] == "":
                        newvalues[x] = y
                    elif y not in newvalues[x]:
                        newvalues[x] = newvalues[x] + ";" + y

        logging.debug(f"update tags {newvalues}")
        result = await db.foto_collection.update_one(myquery, {"$set": newvalues})
        logging.info(f"updated one {result}")


def get_seconds_diff(time1: str, time2: str) -> int:
    """Compare time1 and time2, return time diff in min."""
    seconds_diff = 1000
    t1 = datetime.datetime.strptime("1", "%S")  # nitialize time to zero
    t2 = datetime.datetime.strptime("1", "%S")
    # TODO: Move to properties
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

    seconds_diff = int((t1 - t2).total_seconds())

    return seconds_diff


async def find_info_from_startnummer(db: Any, startnummer: str, tid: str) -> dict:
    """Analyse photo tags and identify heat."""
    nye_tags = {}
    funnetheat = ""
    funnetdeltaker = {}

    starter = await StartListeService().get_startliste_by_nr(db, startnummer)
    if len(starter) > 0:
        nye_tags["Numbers"] = startnummer
        for start in starter:
            # check startnummer
            logging.debug(f"Start funnet: {start}")
            # check heat (if not already found)
            if funnetheat == "":
                funnetheat = await verify_heat(db, tid, start["Heat"])
                if funnetheat != "":
                    nye_tags["Heat"] = funnetheat
        # Get klubb and klasse
        funnetdeltaker = await DeltakereService().get_deltaker_by_startnr(
            db, startnummer
        )

    if "Startnr" in funnetdeltaker:
        nye_tags["Løpsklasse"] = funnetdeltaker["Løpsklasse"]
        nye_tags["Klubb"] = funnetdeltaker["Klubb"]

    return nye_tags


async def find_event_information(db: Any, tags: dict) -> dict:
    """Analyse photo tags and identify event information."""
    newvalues = {}
    nummere = tags["Numbers"]
    personer = tags["Persons"]
    if personer.isnumeric():
        if int(personer) > 0:
            nummerliste = nummere.split(";")
            for nummer in nummerliste:
                tmp_tags = {}
                tmp_tags = find_info_from_startnummer(db, nummer, tags["DateTime"])
                for x, y in tmp_tags.items():
                    logging.debug(f"Found tag: {x}, {y}")
                    if x not in newvalues.keys():
                        newvalues[x] = y
                    elif newvalues[x] == "":
                        newvalues[x] = y
                    elif y not in newvalues[x]:
                        newvalues[x] = newvalues[x] + ";" + y

            texts = tags["Texts"]
            liste = texts.split(";")
            for text in liste:
                if text in klubber:
                    if text not in newvalues["Klubb"]:
                        newvalues["Klubb"] = newvalues["Klubb"] + text + ";"

    return newvalues


async def verify_heat(db: Any, datetime_foto: str, heat_index: str) -> str:
    """Analyse photo tags and identify heat."""
    funnetheat = ""
    lopsdato = await InnstillingerService().get_dato(db)
    tmplopsvarighet = await InnstillingerService().get_lopsvarighet(db)
    # TODO: Move to properties
    lopsvarighet = 180
    if tmplopsvarighet.isnumeric():
        lopsvarighet = int(tmplopsvarighet)

    if datetime_foto is not None:
        heat = await KjoreplanService().get_heat_by_index(db, heat_index)
        if heat is not None:
            seconds = get_seconds_diff(datetime_foto, lopsdato + " " + heat["Start"])
            logging.debug(
                f"Verify heat, diff: {seconds}, heat: {lopsdato} {heat}, foto: {datetime_foto}"
            )
            if -300 < seconds < (300 + lopsvarighet):
                logging.debug(f"Funnet heat: {heat}")
                funnetheat = heat["Index"]

    return funnetheat


async def find_lopsklasse(db: Any, tags: dict) -> str:
    """Analyse photo tags and identify løpsklasse."""
    funnetklasse = ""
    alleklasser = await KlasserService().get_all_klasser(db)
    for klasse in alleklasser:
        logging.debug(klasse)
        if tags["Filename"].find(klasse["Løpsklasse"]) > -1:
            funnetklasse = klasse["Løpsklasse"]
            logging.debug(f"Found klasse: {funnetklasse}")

    return funnetklasse
