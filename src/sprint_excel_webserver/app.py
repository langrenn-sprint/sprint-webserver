"""Package for exposing validation endpoint."""
import logging
import os

from aiohttp import web
import aiohttp_jinja2
import jinja2
import motor.motor_asyncio

from .views import Ping, Ready, Main, Start, Resultat, Live


async def create_app() -> web.Application:
    """Create an web application."""
    app = web.Application()
    # Set up static path
    static_path = os.path.join(os.getcwd(), "src/sprint_excel_webserver/static")
    # Set up template path
    template_path = os.path.join(os.getcwd(), "src/sprint_excel_webserver/templates")
    aiohttp_jinja2.setup(
        app,
        enable_async=True,
        loader=jinja2.FileSystemLoader(template_path),
    )
    logging.error(template_path)
    # Set up database connection:
    client = motor.motor_asyncio.AsyncIOMotorClient()
    db = client.test_database
    app["db"] = db
    app.add_routes(
        [
            web.view("/ping", Ping),
            web.view("/ready", Ready),
            web.view("/", Main),
            web.view("/start", Start),
            web.view("/resultat", Resultat),
            web.view("/live", Live),
            web.static("/static", static_path),
        ]
    )
    # logging configurataion:
    # TODO: get level from environment and set default to INFO
    logging.basicConfig(level=logging.INFO)
    return app
