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
        startliste = await StartListeService().get_all_startlister(
            self.request.app["db"],
        )

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
        await StartListeService().create_startliste(self.request.app["db"], body)
        return web.Response(status=201)
