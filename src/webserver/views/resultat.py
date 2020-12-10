"""Resource module for resultat view."""
# import logging

from aiohttp import web

# import aiohttp_jinja2


class Resultat(web.View):
    """Class representing the resultat view."""

    async def get(self) -> web.Response:
        """Get route function."""
        return "Resultat! Heat: " + self.request.args.get("heat") + ".\n"
