"""Resource module for main view."""
# import logging

from aiohttp import web
import aiohttp_jinja2


# TODO: klasser objektet bør leses fra csv fil.
klasser = [
    {"klasse": "Menn junior", "lopsklasse": "MJ", "rekkefolge": "1"},
    {"klasse": "G 16 år", "lopsklasse": "G16", "rekkefolge": "2"},
]

# TODO: kjoreplan objektet bør leses fra csv fil.
kjoreplan = [
    {
        "lopsklasse": "MJ",
        "index": "MJSA1",
        "runde": "Semifinale A - Heat 1",
        "starttid": "09:00",
    },
    {
        "lopsklasse": "MJ",
        "index": "MJSA2",
        "runde": "Semifinale A - Heat 2",
        "starttid": "09:03",
    },
]


class Main(web.View):
    """Class representing the main view."""

    async def get(self) -> web.Response:
        """Get route function."""
        return await aiohttp_jinja2.render_template_async(
            "index.html",
            self.request,
            {"klasser": klasser, "kjoreplan": kjoreplan},
        )
