import os
import discord
import requests

from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv

load_dotenv()
wHook = os.getenv('DISCORD_WEBHOOK')

webhook = Webhook.from_url(wHook, adapter=RequestsWebhookAdapter())
#webhook.send("Hello")
