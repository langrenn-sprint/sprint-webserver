"""Resource module for live view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    DeltakereService,
    KjoreplanService,
    KlasserService,
    StartListeService,
)


class Live(web.View):
    """Class representing the live view."""

    async def get(self) -> web.Response:
        """Get route function that return the live result page."""
        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
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

        startliste = []
        kjoreplan = []
        if valgt_startnr == "":
            tmp = await StartListeService().get_startliste_by_klasse(
                self.request.app["db"], valgt_klasse
            )
            # filter out garbage
            for start in tmp:
                if str(start["Nr"]).isnumeric():
                    startliste.append(start)

            kjoreplan = await KjoreplanService().get_heat_by_klasse(
                self.request.app["db"], valgt_klasse
            )
        else:
            # only selected racer
            valgt_startnr = valgt_startnr.replace(".0", "")
            startliste = await StartListeService().get_startliste_by_nr(
                self.request.app["db"],
                valgt_startnr,
            )
            for heat in startliste:
                tmp = await KjoreplanService().get_heat_by_index(
                    self.request.app["db"],
                    heat["Heat"],
                )
                kjoreplan.append(tmp)
            valgt_startnr = "Startnr: " + valgt_startnr + ", "

        # format time
        for heat in kjoreplan:
            # Format time from decimal to readable format hh:mm:ss:
            time = heat["Start"].replace(",", ".")
            heat["Start"] = _format_time(time)

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "live.html",
            self.request,
            {
                "valgt_klasse": valgt_klasse,
                "valgt_startnr": valgt_startnr,
                "klasser": klasser,
                "deltakere": deltakere,
                "kjoreplan": kjoreplan,
                "startliste": startliste,
            },
        )


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
