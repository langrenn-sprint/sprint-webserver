"""Resource module for resultat view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    FotoService,
    InnstillingerService,
    KjoreplanService,
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
    """Class representing the resultat view. Both sluttresultat and heatresultat."""

    async def get(self) -> web.Response:
        """Get route function."""
        _lopsinfo = await InnstillingerService().get_header_footer_info(
            self.request.app["db"],
        )
        logging.debug(_lopsinfo)

        foto = []
        informasjon = ""
        resultatliste = []
        heatliste = []
        resultatheatliste = []
        valgt_lopsklasse = ""
        valgt_bildevisning = ""

        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
            logging.debug(valgt_klasse)
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
            if klasse["Klasse"] == valgt_klasse:
                valgt_lopsklasse = klasse["Løpsklasse"]

        if (valgt_klasse == "") and (valgt_klubb == ""):
            informasjon = "Velg klasse eller klubb for å vise resultater"
        elif valgt_klasse == "":
            # get resultat by klubb
            resultatliste = await ResultatService().get_resultatliste_by_klubb(
                self.request.app["db"],
                valgt_klubb,
            )
            foto = await FotoService().get_foto_by_klubb(
                self.request.app["db"], valgt_klubb
            )
            valgt_bildevisning = "klubb=" + valgt_klubb
        else:
            # get resultat by klasse - sluttresultat
            resultatliste = await ResultatService().get_resultatliste_by_klasse(
                self.request.app["db"],
                valgt_klasse,
            )
            # heatresultater
            lopsklasse = await KlasserService().get_lopsklasse_for_klasse(
                self.request.app["db"],
                valgt_klasse,
            )
            heatliste = await KjoreplanService().get_heat_by_klasse(
                self.request.app["db"],
                lopsklasse,
            )
            resultatheatliste = await ResultatHeatService().get_resultatheat_by_klasse(
                self.request.app["db"],
                lopsklasse,
            )
            foto = await FotoService().get_foto_by_klasse(
                self.request.app["db"], valgt_lopsklasse
            )
            valgt_bildevisning = "klasse=" + valgt_lopsklasse

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "resultat.html",
            self.request,
            {
                "foto": foto,
                "informasjon": informasjon,
                "lopsinfo": _lopsinfo,
                "valgt_bildevisning": valgt_bildevisning,
                "valgt_klasse": valgt_klasse,
                "valgt_klubb": valgt_klubb,
                "klasser": klasser,
                "klubber": klubber,
                "resultatliste": resultatliste,
                "heatliste": heatliste,
                "resultatheatliste": resultatheatliste,
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
