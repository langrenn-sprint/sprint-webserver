"""Resource module for main view."""
import logging

from aiohttp import web
import aiohttp_jinja2

from sprint_webserver.services import KjoreplanService, KlasserService


class Main(web.View):
    """Class representing the main view."""

    async def get(self) -> web.Response:
        """Get route function that return the main page."""
        klasser = await KlasserService().get_all_klasser(self.request.app["db"])
        kjoreplan = await KjoreplanService().get_all_heat(self.request.app["db"])

        # format time
        for heat in kjoreplan:
            # Format time from decimal to readable format hh:mm:ss:
            time = heat["Start"].replace(",", ".")
            heat["Start"] = _format_time(time)

        return await aiohttp_jinja2.render_template_async(
            "index.html",
            self.request,
            {"klasser": klasser, "kjoreplan": kjoreplan},
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
