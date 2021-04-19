"""Resource module for foto view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import (
    FotoService,
    InnstillingerService,
    KlasserService,
    StartListeService,
)

lokasjoner = [
    "Start",
    "Mål",
    "Målfoto",
    "Premie",
]


class AdminFoto(web.View):
    """Class representing the Foto admin resource."""

    async def get(self) -> web.Response:
        """Get route function that returns all foto."""
        _lopsinfo = await InnstillingerService().get_header_footer_info(
            self.request.app["db"],
        )

        try:
            valgt_klasse = self.request.rel_url.query["klasse"]
        except Exception:
            valgt_klasse = ""  # noqa: F841

        # hente valgte foto
        foto = []
        if valgt_klasse == "":
            foto = await FotoService().get_all_foto(self.request.app["db"])
        else:
            foto = await FotoService().get_foto_by_klasse(
                self.request.app["db"], valgt_klasse
            )
        logging.debug(len(foto))

        # hente alle klasser
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])

        # hente heat-deltakere
        heatliste = {}
        for one_foto in foto:
            if "Heat" in one_foto.keys():
                if not one_foto["Heat"] == "":
                    startliste = await StartListeService().get_startliste_by_heat(
                        self.request.app["db"], one_foto["Heat"]
                    )
                    logging.debug(f"Hentet heat: {startliste}")
                    heatliste[one_foto["Heat"]] = startliste

        # ensure web safe urls
        for klasse in klasser:
            klasse["KlasseWeb"] = klasse["Klasse"].replace(" ", "%20")

        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "adm_foto.html",
            self.request,
            {
                "foto": foto,
                "heatliste": heatliste,
                "klasser": klasser,
                "lokasjoner": lokasjoner,
                "lopsinfo": _lopsinfo,
                "valgt_klasse": valgt_klasse,
            },
        )

    async def post(self) -> web.Response:
        """Post route function."""
        tags = {}
        try:
            form_data = await self.request.post()
            tags["DateTime"] = form_data["DateTime"]
            tags["Filename"] = form_data["Filename"]
            tags["Lokasjon"] = form_data["Lokasjon"]
            tags["Løpsklasse"] = form_data["Løpsklasse"]
            tags["Numbers"] = form_data["Numbers"]
            tags["OldNumbers"] = form_data["OldNumbers"]

        except Exception:
            logging.error("Error parsing request parameters.")
            raise web.HTTPBadRequest

        logging.debug(f"Got tags: {tags}")
        await FotoService().update_tags(self.request.app["db"], tags)

        raise web.HTTPFound("/admin/foto?informasjon=Oppdatert")

    async def put(self) -> web.Response:
        """Post route function."""
        # TODO: legge inn database-kall
        raise web.HTTPNotImplemented
