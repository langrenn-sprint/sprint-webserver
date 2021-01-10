"""Resource module for resultat view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    KlasserService,
    ResultatHeatService,
    ResultatService,
)

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


class Resultat(web.View):
    """Class representing the resultat view."""

    async def get(self) -> web.Response:
        """Get route function."""
        informasjon = ""
        resultatliste = []
        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
            logging.info(valgt_klasse)
        except Exception:
            valgt_klasse = ""  # noqa: F841
        try:
            valgt_klubb = self.request.rel_url.query["klubb"]
        except Exception:
            valgt_klubb = ""

        klasser = await KlasserService().get_all_klasser(self.request.app["db"])
        # ensure web safe urls
        for klasse in klasser:
            klasse["KlasseWeb"] = klasse["Klasse"].replace(" ", "%20")

        if (valgt_klasse == "") and (valgt_klubb == ""):
            informasjon = "Velg klasse eller klubb for å vise resultater"
        elif valgt_klasse == "":
            # get resultat by klubb
            resultatliste = await ResultatService().get_resultatliste_by_klubb(
                self.request.app["db"],
                valgt_klubb,
            )
            # clean data
            for loper in resultatliste:
                loper["Nr"] = str(loper["Nr"]).replace(".0", "")
                loper["Plass"] = str(loper["Plass"]).replace(".0", "")
        else:
            # get resultat by klasse
            resultatliste = await ResultatService().get_resultatliste_by_klasse(
                self.request.app["db"],
                valgt_klasse,
            )
            # clean data
            for loper in resultatliste:
                loper["Nr"] = str(loper["Nr"]).replace(".0", "")
                loper["Plass"] = str(loper["Plass"]).replace(".0", "")

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "resultat.html",
            self.request,
            {
                "informasjon": informasjon,
                "valgt_klasse": valgt_klasse,
                "valgt_klubb": valgt_klubb,
                "klasser": klasser,
                "klubber": klubber,
                "resultatliste": resultatliste,
            },
        )

    async def post(self) -> web.Response:
        """Post route function that creates a collection of athletes."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        result = await ResultatService().create_resultatliste(
            self.request.app["db"], body
        )
        return web.Response(status=result)


class ResultatHeat(web.View):
    """Class representing the resultat heat view."""

    async def post(self) -> web.Response:
        """Post route function that creates a collection of athletes."""
        body = await self.request.json()
        logging.debug(f"Got request-body {body} of type {type(body)}")
        result = await ResultatHeatService().create_resultatheat(
            self.request.app["db"], body
        )
        return web.Response(status=result)
