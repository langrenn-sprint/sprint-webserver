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

        # format time
        for heat in body:
            # Format time from decimal to readable format hh:mm:ss:
            time = heat["Start"].replace(",", ".")
            heat["Start"] = _format_time(time)

        # if kjøreplan is updated, only change the heats without resultat_registrert
        if "kjoreplan_collection" in collist:
            returncode = 202
            for heat in body:
                result = await db.kjoreplan_collection.find_one(
                    {"Index": heat["Index"]}
                )
                logging.debug(heat["Index"])

                if result["resultat_registrert"]:
                    # resultat registrert - heat kan ikke endres
                    logging.info("Ignorert: " + result["Index"])
                else:
                    result = await db.kjoreplan_collection.update_one(
                        {"Index": heat["Index"]}, {"$set": heat}
                    )
                    logging.debug(result)
        else:
            result = await db.kjoreplan_collection.insert_many(body)
            logging.debug("inserted %d docs" % (len(result.inserted_ids),))
            _newvalue = {"resultat_registrert": False}
            result = await db.kjoreplan_collection.update_many({}, {"$set": _newvalue})
            logging.debug(result)

        # update tidplan if kjøreplan exists
        if "klasser_collection" in collist:
            await KjoreplanService().update_tidplan(db)
            logging.debug("Updating tidplan")

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

    async def update_tidplan(self, db: Any) -> int:
        """Update tidplan function. Will update klasser object, requires Kjøreplan created."""
        returncode = 201

        # get klasser
        klasser = []
        cursor = db.klasser_collection.find()
        for document in await cursor.to_list(length=100):
            klasser.append(document)

        # get heat
        kjoreplan = []
        cursor = db.kjoreplan_collection.find()
        for document in await cursor.to_list(length=500):
            kjoreplan.append(document)

        # loop through klasser and kjøreplan - update start time pr round
        for klasse in klasser:
            klasse["SemiC"] = False
            klasse["FinaleC"] = False
            klasse["FinaleB"] = False
            for heat in kjoreplan:
                if klasse["Løpsklasse"] == heat["Løpsklasse"]:
                    if heat["Heat"] == "KA1":
                        _myquery = {"Klasse": klasse["Klasse"]}
                        _newvalue = {"TidKvart": heat["Start"]}
                        result = await db.klasser_collection.update_one(
                            _myquery, {"$set": _newvalue}
                        )
                        logging.debug(result)
                        returncode = 202
                    elif heat["Heat"] == "SC1":
                        _myquery = {"Klasse": klasse["Klasse"]}
                        _newvalue = {"TidSemi": heat["Start"]}
                        result = await db.klasser_collection.update_one(
                            _myquery, {"$set": _newvalue}
                        )
                        logging.debug(result)
                        klasse["SemiC"] = True
                    elif heat["Heat"] == "SA1":
                        if klasse["SemiC"] is False:
                            _myquery = {"Klasse": klasse["Klasse"]}
                            _newvalue = {"TidSemi": heat["Start"]}
                            result = await db.klasser_collection.update_one(
                                _myquery, {"$set": _newvalue}
                            )
                            logging.debug(result)
                    elif heat["Heat"] == "FC":
                        _myquery = {"Klasse": klasse["Klasse"]}
                        _newvalue = {"TidFinale": heat["Start"]}
                        result = await db.klasser_collection.update_one(
                            _myquery, {"$set": _newvalue}
                        )
                        klasse["FinaleC"] = True
                        logging.debug(result)
                    elif heat["Heat"] == "FB":
                        klasse["FinaleB"] = True
                        if klasse["FinaleC"] is False:
                            _myquery = {"Klasse": klasse["Klasse"]}
                            _newvalue = {"TidFinale": heat["Start"]}
                            result = await db.klasser_collection.update_one(
                                _myquery, {"$set": _newvalue}
                            )
                            logging.debug(result)
                    elif heat["Heat"] == "FA":
                        if (klasse["FinaleC"] or klasse["FinaleB"]) is False:
                            _myquery = {"Klasse": klasse["Klasse"]}
                            _newvalue = {"TidFinale": heat["Start"]}
                            result = await db.klasser_collection.update_one(
                                _myquery, {"$set": _newvalue}
                            )
                            logging.debug(result)
                    elif heat["Heat"] == "F1":
                        _myquery = {"Klasse": klasse["Klasse"]}
                        _newvalue = {"TidKvart": heat["Start"]}
                        result = await db.klasser_collection.update_one(
                            _myquery, {"$set": _newvalue}
                        )
                        logging.debug(result)
                    elif heat["Heat"] == "A1":
                        _myquery = {"Klasse": klasse["Klasse"]}
                        _newvalue = {"TidSemi": heat["Start"]}
                        result = await db.klasser_collection.update_one(
                            _myquery, {"$set": _newvalue}
                        )
                        logging.debug(result)

        return returncode


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
