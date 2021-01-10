"""Resource module for start resources."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    KjoreplanService,
    KlasserService,
    StartListeService,
)


class Start(web.View):
    """Class representing the start view."""

    async def get(self) -> web.Response:
        """Get route function that return the startlister page."""
        informasjon = ""
        startliste = []

        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
        except Exception:
            valgt_klasse = ""  # noqa: F841
            informasjon = "Velg klasse for å se startlister."
        try:
            valgt_heat = self.request.rel_url.query["heat"]
        except Exception:
            valgt_heat = ""  # noqa: F841

        kjoreplan = await KjoreplanService().get_heat_by_klasse(
            self.request.app["db"], valgt_klasse
        )
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        _liste = await StartListeService().get_startliste_by_lopsklasse(
            self.request.app["db"], valgt_klasse
        )
        logging.debug(_liste)

        # filter out garbage
        for start in _liste:
            start["Pos"] = str(start["Pos"]).replace(".0", "")
            start["Nr"] = str(start["Nr"]).replace(".0", "")
            logging.debug(start["Nr"])
            if str(start["Nr"]).isnumeric() and (int(start["Nr"]) > 0):
                startliste.append(start)

        # format time
        for heat in kjoreplan:
            # Format time from decimal to readable format hh:mm:ss:
            time = heat["Start"].replace(",", ".")
            heat["Start"] = _format_time(time)

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "start.html",
            self.request,
            {
                "informasjon": informasjon,
                "valgt_klasse": valgt_klasse,
                "valgt_heat": valgt_heat,
                "klasser": klasser,
                "kjoreplan": kjoreplan,
                "startliste": startliste,
            },
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of athletes."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        result = await StartListeService().create_startliste(
            self.request.app["db"], body
        )
        return web.Response(status=result)


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
