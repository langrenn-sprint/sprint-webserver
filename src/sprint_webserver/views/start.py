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
        kjoreplan = []
        klassetider = {}
        colseparators = []
        colclass = "w3-third"

        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
        except Exception:
            valgt_klasse = ""  # noqa: F841
            informasjon = "Velg klasse for å se startlister."
        try:
            valgt_heat = self.request.rel_url.query["heat"]
        except Exception:
            valgt_heat = ""  # noqa: F841

        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        if valgt_klasse == "live":
            # vis heat som starter nå
            iantallheat = 10
            isplitt = [3, 6]
            kjoreplan = await KjoreplanService().get_upcoming_heat(
                self.request.app["db"], iantallheat
            )
            i = 0
            for heat in kjoreplan:
                logging.debug(heat["Index"])
                _liste = await StartListeService().get_startliste_by_heat(
                    self.request.app["db"], heat["Index"]
                )
                if i in isplitt:
                    colseparators.append(heat["Index"])
                    logging.debug(colseparators)
                i += 1
                for loper in _liste:
                    startliste.append(loper)
                logging.debug(startliste)
        else:
            # get startlister for klasse
            klassetider = await KlasserService().get_klasse_by_lopsklasse(
                self.request.app["db"], valgt_klasse
            )
            kjoreplan = await KjoreplanService().get_heat_by_klasse(
                self.request.app["db"], valgt_klasse
            )
            startliste = await StartListeService().get_startliste_by_lopsklasse(
                self.request.app["db"], valgt_klasse
            )
        logging.debug(startliste)

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "start.html",
            self.request,
            {
                "informasjon": informasjon,
                "valgt_klasse": valgt_klasse,
                "valgt_heat": valgt_heat,
                "colseparators": colseparators,
                "colclass": colclass,
                "klasser": klasser,
                "klassetider": klassetider,
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
