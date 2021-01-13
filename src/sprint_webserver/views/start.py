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
