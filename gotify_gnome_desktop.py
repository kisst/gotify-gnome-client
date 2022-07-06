#!/usr/bin/env python3
"""
simple gotify to gnome toast application
"""
import asyncio
import configparser
import os
from gotify import AsyncGotify
from gi import require_version

require_version("Notify", "0.7")
from gi.repository import Notify

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

SERVER_URL = config["DEFAULT"]["SERVER_URL"]
API_KEY = config["DEFAULT"]["API_KEY"]


async def push_messages():
    """
    fetch messages from gotify and send to gnome
    """
    async_gotify = AsyncGotify(base_url=SERVER_URL, client_token=API_KEY)

    async for msg in async_gotify.stream():
        message = str(msg["title"]) + ' says "' + msg["message"] + '"'
        Notify.init("Gotify")
        Notify.Notification.new(message).show()


asyncio.run(push_messages())

Notify.init("Gotify-client")
Notify.Notification.new("Message fetching stopped...").show()
