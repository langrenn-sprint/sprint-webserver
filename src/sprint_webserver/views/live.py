"""Resource module for live view."""
# import logging

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

        kjoreplan = await KjoreplanService().get_heat_by_klasse(
            self.request.app["db"], valgt_klasse
        )
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        deltakere = await DeltakereService().get_deltakere_by_lopsklasse(
            self.request.app["db"], valgt_klasse
        )

        if valgt_startnr == "":
            startliste = await StartListeService().get_all_startlister(
                self.request.app["db"],
            )
        else:
            startliste = await StartListeService().get_startliste_by_nr(
                self.request.app["db"],
                valgt_startnr,
            )

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
