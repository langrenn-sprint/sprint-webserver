"""Resource module for live view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    DeltakereService,
    KjoreplanService,
    KlasserService,
    ResultatHeatService,
    StartListeService,
)


class Live(web.View):
    """Class representing the live view."""

    # TODO: reduser kompleksistet i denne funksjonen
    async def get(self) -> web.Response:  # noqa: C901
        """Get route function that return the live result page."""
        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
            logging.debug(valgt_klasse)
        except Exception:
            valgt_klasse = ""

        try:
            valgt_startnr = self.request.rel_url.query["startnr"]
        except Exception:
            valgt_startnr = ""

        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        deltakere = await DeltakereService().get_deltakere_by_lopsklasse(
            self.request.app["db"], valgt_klasse
        )
        logging.debug(deltakere)

        kjoreplan = []
        startliste = []
        resultatliste = []
        colseparators = []
        colclass = "w3-third"
        if valgt_startnr == "":

            kjoreplan = await KjoreplanService().get_heat_for_live_scroll(
                self.request.app["db"], valgt_klasse
            )

            # responsive design - determine column-arrangement
            colseparators = ["KA1", "KA5", "SC1", "SA1", "F1", "F5", "A1", "A5"]
            icolcount = 0
            for heat in kjoreplan:
                if heat["Heat"] in colseparators:
                    icolcount += 1
                    if (heat["Heat"] == "SC1") and heat["resultat_registrert"]:
                        colseparators.remove("SC1")
                elif heat["Heat"] in {"FA", "FB", "FC"}:
                    icolcount += 1
                    colseparators.append(heat["Heat"])
                    break
            if icolcount == 4:
                colclass = "w3-quart"
            colseparators.remove("KA1")
            colseparators.remove("F1")

            _liste = await StartListeService().get_startliste_by_lopsklasse(
                self.request.app["db"], valgt_klasse
            )
            logging.debug(_liste)

            # filter out garbage and clean data
            for start in _liste:
                logging.debug(start["Nr"])
                if str(start["Nr"]).isnumeric() and (int(start["Nr"]) > 0):
                    startliste.append(start)
            logging.debug(startliste)

            _liste = await ResultatHeatService().get_resultatheat_by_klasse(
                self.request.app["db"], valgt_klasse
            )
            # filter out garbage
            for res in _liste:
                if str(res["Nr"]).isnumeric() and (int(res["Nr"]) > 0):
                    resultatliste.append(res)

        else:
            # only selected racer
            logging.debug(valgt_startnr)

            startliste = await StartListeService().get_startliste_by_nr(
                self.request.app["db"],
                valgt_startnr,
            )
            logging.debug(startliste)

            for start in startliste:
                _heat = await KjoreplanService().get_heat_by_index(
                    self.request.app["db"],
                    start["Heat"],
                )
                kjoreplan.append(_heat)

            # check for resultat
            resultatliste = await ResultatHeatService().get_resultatheat_by_nr(
                self.request.app["db"],
                valgt_startnr,
            )

            valgt_startnr = "Startnr: " + valgt_startnr + ", "

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "live.html",
            self.request,
            {
                "valgt_klasse": valgt_klasse,
                "valgt_startnr": valgt_startnr,
                "colseparators": colseparators,
                "colclass": colclass,
                "klasser": klasser,
                "deltakere": deltakere,
                "kjoreplan": kjoreplan,
                "resultatliste": resultatliste,
                "startliste": startliste,
            },
        )
